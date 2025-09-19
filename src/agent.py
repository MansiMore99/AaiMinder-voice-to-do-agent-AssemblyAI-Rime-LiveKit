# src/agent.py
import logging
from dotenv import load_dotenv

from livekit.agents import (
    NOT_GIVEN,
    Agent,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# If you are using your own AssemblyAI/Rime keys (recommended), import plugins:
#   pip install "livekit-agents[assemblyai]~=1.2" "livekit-agents[rime]~=1.2"
from livekit.plugins import assemblyai, rime

# For tool definitions
from livekit.agents import function_tool, RunContext
from skills.todo import TodoStore

logger = logging.getLogger("agent")
load_dotenv(".env.local")  # loads LIVEKIT_*, ASSEMBLYAI_API_KEY, RIME_API_KEY

# Shared store instance
store = TodoStore()


class TodoAgent(Agent):
    """
    Voice-first to-do & reminder assistant.
    The LLM routes user requests to the three tools below.
    Keep responses brief and confirm destructive actions.
    """

    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a concise, friendly voice to-do assistant. "
                "Use the available tools to add, list, and complete tasks. "
                "Always confirm before marking a task complete. "
                "If a request is unclear, ask a short follow-up. "
                "Keep replies under one sentence."
            )
        )

    async def on_enter(self):
        # Spoken welcome when the session starts
        await self.session.say(
            "Hi! Say add buy milk, read my tasks, or mark milk done."
        )

    # ---------- Tools ----------

    @function_tool(
        name="add_task",
        description="Add a task. Include optional due date string like 2025-09-20.",
    )
    async def add_task(
        self, context: RunContext, text: str, due: str | None = None
    ) -> dict:
        tid = store.add(text, due)
        return {"id": tid, "text": text, "due": due}

    @function_tool(name="list_tasks", description="List up to 10 pending tasks.")
    async def list_tasks(self, context: RunContext) -> dict:
        tasks = store.list_open()[:10]
        return {"tasks": tasks}

    @function_tool(
        name="complete_task",
        description="Complete a task by id or matching text. Must confirm with user first.",
    )
    async def complete_task(self, context: RunContext, query: str) -> dict:
        # Expect the LLM to ask for confirmation before calling this
        task = store.complete(query)
        return {"ok": bool(task), "task": task}


def prewarm(proc: JobProcess):
    # Load VAD once per worker for faster cold start
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Enrich logs
    ctx.log_context_fields = {"room": ctx.room.name}

    # Build a voice pipeline using AssemblyAI (STT) + Rime (TTS).
    # This version uses *your* AssemblyAI/Rime accounts via plugins.
    session = AgentSession(
        # If you prefer LiveKit Cloud defaults instead of your own keys:
          stt="assemblyai",
          tts="rime/arcana:luna",
        # otherwise use plugin-based:
        #stt=assemblyai.STT(interim_results=True),
        # tts=rime.TTS(model="arcana", speaker="luna"),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
        # LLM:
        # Keep Azure GPT-4o-mini from the template; you can change via env/LiveKit project.
        llm="azure/gpt-4o-mini",
    )

    # Handle false-positive interruptions (resume TTS if noise cut us off)
    @session.on("agent_false_interruption")
    def _on_agent_false_interruption(ev: AgentFalseInterruptionEvent):
        logger.info("False positive interruption, resuming.")
        session.generate_reply(instructions=ev.extra_instructions or NOT_GIVEN)

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start pipeline and connect
    await session.start(
        agent=TodoAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()

    # Friendly intro line (non-interruptible)
    await session.generate_reply(
        instructions=(
            "Welcome the user. Offer one-sentence help: "
            "Say add buy milk, read my tasks, or mark milk done."
        ),
        allow_interruptions=False,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
