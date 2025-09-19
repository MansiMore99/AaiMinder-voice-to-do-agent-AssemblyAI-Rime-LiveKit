AaiMinder — Voice To-Do & Reminder Agent

A voice-controlled to-do assistant using AssemblyAI (STT) + Rime (TTS) on LiveKit Agents.

✨ What it does

Speak naturally:

“add buy milk”

“read my tasks”

“mark milk done”

AaiMinder transcribes your voice (AssemblyAI), manages tasks locally (tasks.json), and replies out loud (Rime).

🧱 Architecture

LiveKit Agents: real-time voice agent runtime

AssemblyAI: streaming speech-to-text (STT)

Rime: low-latency text-to-speech (TTS)

Local store: tasks.json (no DB needed)

Mic → LiveKit Room → AssemblyAI (STT) → Agent (tools) → TodoStore → Rime (TTS) → Speaker

📦 Requirements

Python 3.10+

uv (Python package manager)

LiveKit Cloud project (URL + API key/secret)

ASSEMBLYAI_API_KEY

RIME_API_KEY

⚙️ Setup

Clone & enter the repo

git clone <your-fork-or-local-repo-url>
cd voice-agent-hackathon


Install deps

uv sync
uv pip install -U livekit-agents
uv add "livekit-agents[assemblyai]~=1.2" "livekit-agents[rime]~=1.2"


Environment

cp .env.example .env.local


Fill in:

LIVEKIT_URL=...           # from LiveKit Cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...

ASSEMBLYAI_API_KEY=...
RIME_API_KEY=...

🗂️ Project Structure (key files)
src/
  agent.py           # AaiMinder agent: STT/TTS wiring + tools exposure
  skills/
    todo.py          # Tiny JSON-backed task store (add/list/complete)

tasks.json           # Created at runtime (git-ignored recommended)
.env.local           # Your secrets (never commit)

🚀 Run (dev)

Warm required models (VAD / turn detector):

uv run python src/agent.py download-files


Start the agent (dev mode):

uv run python src/agent.py dev


Open AaiMinder & talk

In your LiveKit Cloud Console, open Agents → Playground.

Ensure the Playground uses the same project (matches your LIVEKIT_* in .env.local).

Click Start / Connect — the Playground creates a room and starts a job; your local worker (running via the command above) will pick it up.

Grant mic permissions in the browser and speak:

“add buy milk”

“read my tasks”

“mark milk done”

Tip: keep your terminal visible — you’ll see logs and any tool calls (add/list/complete).

🧪 Example Voice Script (for demo)

You: “add buy milk”

Agent: “added buy milk”

You: “read my tasks”

Agent: “you have one task: buy milk”

You: “mark milk done”

Agent: “marked buy milk done”

🛠️ Implementation Notes
STT / TTS

src/agent.py wires:

stt=assemblyai.STT(interim_results=True)

tts=rime.TTS(model="arcana", speaker="luna")

Tools (no custom parsing needed)

TodoAgent exposes 3 tools the LLM calls:

add_task(text, due=None)

list_tasks()

complete_task(query) (instructed to confirm before marking done)

Task Store

src/skills/todo.py uses a tiny JSON store:

{
  "tasks": [
    { "id": 1712345678901, "text": "buy milk", "done": false, "due": null }
  ]
}

🧹 .gitignore (recommendation)

Add:

tasks.json
.env.local

🐛 Troubleshooting

ImportError: RunContext
Import RunContext from livekit.agents (not .llm) and ensure you’ve upgraded livekit-agents.

No audio / mic
Allow mic access in the browser; reconnect the Playground.

TTS/voice doesn’t change
Ensure you’re using the plugin-based TTS:
tts=rime.TTS(model="arcana", speaker="luna")
(and that RIME_API_KEY is set).

STT laggy
Keep interim_results=True for AssemblyAI.

Tools not triggering
Make sure @function_tool decorators are present and your instructions explicitly tell the model to use tools for add/list/complete.

🧭 Next Steps (optional polish)

Reminders: add a remind_in(seconds, text) tool that schedules a delayed session.say(text).

Due dates: light NLP for “tomorrow / in 2 hours” → normalize date string and pass to add_task(...).

Google Sheets: swap JSON store for a sheet if you want cloud persistence.
