<!--
  AaiMinder — README
  Tip: put a wide hero image at: assets/banner_aaiminder.png  (1600x600+)
-->

<h1 align="center">📝 AaiMinder — Voice To-Do & Reminder Agent</h1>

<p align="center">
  <em>Voice-controlled to-do assistant powered by AssemblyAI (STT) + Rime (TTS) on LiveKit Agents.</em>
</p>

<p align="center">
  <img src="<img width="391" height="456" alt="image" src="https://github.com/user-attachments/assets/07741c67-290f-462f-982e-c857067b0bbe">
</p>

<p align="center">
  <a href="https://cloud.livekit.io" target="_blank"><img src="https://img.shields.io/badge/LiveKit-Agents-0E7B7B?logo=livekit&logoColor=white" alt="LiveKit Agents"></a>
  <a href="https://www.assemblyai.com/" target="_blank"><img src="https://img.shields.io/badge/AssemblyAI-STT-5856D6" alt="AssemblyAI"></a>
  <a href="https://docs.rime.ai" target="_blank"><img src="https://img.shields.io/badge/Rime-TTS-8E44AD" alt="Rime"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-2ECC71" alt="MIT">
</p>

---

## 📋 Overview

AaiMinder lets you **speak your tasks** and hear quick confirmations.  
It **transcribes** with AssemblyAI, **manages tasks** locally in `tasks.json`, and **speaks back** using Rime.

> 💡 Best for a hackathon demo: tangible, fast, and no database setup.

---

## Setup

Step 1: Copy this repository (Click the green "Use this template" button on GitHub)  
Step 2: Clone your new copy to your local machine  
Step 3: Install dependencies using uv ([install uv here](https://docs.astral.sh/uv/getting-started/installation/) if needed)  

```shell
cd voice-agent-hackathon
uv sync
```

Step 4: Set up the environment by copying `.env.example` to `.env.local` and filling in the required values from your [LiveKit Cloud](https://cloud.livekit.io) project

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

You can load the LiveKit environment automatically using the [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup):

```bash
lk cloud auth
lk app env -w -d .env.local
```

## Run the agent

Before your first run, you must download certain models such as [Silero VAD](https://docs.livekit.io/agents/build/turns/vad/) and the [LiveKit turn detector](https://docs.livekit.io/agents/build/turns/turn-detector/):

```shell
uv run python src/agent.py download-files
```

Next, run this command to start the agent:

```shell
uv run python src/agent.py dev
```

Finally, open the [LiveKit Agents Playground](https://agents-playground.livekit.io/#cam=0&mic=1&screen=0&video=0&audio=1&chat=1&theme_color=cyan) to speak with your new agent!

## Tips for managing background noise

This hackathon may be a noisy place which can make it tricky to test your agent. Here are some tips to help you:

1. Use headphones with a microphone and noise isolation features (such as Airpods) 
2. Use the LiveKit [background voice cancellation](https://docs.livekit.io/home/cloud/noise-cancellation/) model (pre-installed in this template)
3. Turn off your microphone in the [Agents Playground](https://agents-playground.livekit.io/#cam=0&mic=1&screen=0&video=0&audio=1&chat=1&theme_color=cyan) and use text input to test your agent instead.

## Custom frontend & telephony

Get started quickly with our pre-built frontend starter apps, or add telephony support:

| Platform | Link | Description |
|----------|----------|-------------|
| **Web** | [`livekit-examples/agent-starter-react`](https://github.com/livekit-examples/agent-starter-react) | Web voice AI assistant with React & Next.js |
| **iOS/macOS** | [`livekit-examples/agent-starter-swift`](https://github.com/livekit-examples/agent-starter-swift) | Native iOS, macOS, and visionOS voice AI assistant |
| **Flutter** | [`livekit-examples/agent-starter-flutter`](https://github.com/livekit-examples/agent-starter-flutter) | Cross-platform voice AI assistant app |
| **React Native** | [`livekit-examples/agent-starter-react-native`](https://github.com/livekit-examples/agent-starter-react-native) | Native mobile app with React Native & Expo |
| **Android** | [`livekit-examples/agent-starter-android`](https://github.com/livekit-examples/agent-starter-android) | Native Android app with Kotlin & Jetpack Compose |
| **Web Embed** | [`livekit-examples/agent-starter-embed`](https://github.com/livekit-examples/agent-starter-embed) | Voice AI widget for any website |
| **Telephony** | [📚 Documentation](https://docs.livekit.io/agents/start/telephony/) | Add inbound or outbound calling to your agent |

For advanced customization, see the [complete frontend guide](https://docs.livekit.io/agents/start/frontend/).

## Tests and evals

This project includes a complete suite of evals, based on the LiveKit Agents [testing & evaluation framework](https://docs.livekit.io/agents/build/testing/). To run them, use `pytest`.

```shell
uv run pytest
```

To run the tests in a CI environment, you must also [add repository secrets](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/using-secrets-in-github-actions) for `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`.

## Deploying to production

This project is production-ready and includes a working `Dockerfile`. To deploy it to LiveKit Cloud or another environment, see the [deploying to production](https://docs.livekit.io/agents/ops/deployment/) guide.

## Models

This project uses models from AssemblyAI and Rime, as well as GPT-4o-mini from Azure OpenAI. By default, these are served through early-access to LiveKit Inference and no extra account is required.

### AssemblyAI customization

To customize the AssemblyAI model, while still using LiveKit Cloud, you can use the following session setup in your [agent code](https://github.com/livekit-examples/voice-agent-hackathon/blob/main/src/agent.py) instead of the version above:

```python
from livekit.agents import inference

session = AgentSession(
    stt=inference.STT(model="assemblyai", extra_kwargs={ ... })
)
```

Refer to the [source code](https://github.com/livekit/agents/blob/main/livekit-agents/livekit/agents/inference/stt.py#L57) for available parameters (docs for LiveKit Inference are coming soon)

#### AssemblyAI plugin

To use your own AssemblyAI account, or access additional AssemblyAI features, use the AssemblyAI plugin:

```shell
uv add livekit-agents[assemblyai]
```

```python
from livekit.plugins import assemblyai

session = AgentSession(
    stt=assemblyai.STT()
)
```

Refer to the [plugin documentation](https://docs.livekit.io/agents/integrations/stt/assemblyai/) for more information.

### Rime customization

To use a different Rime voice, while still using LiveKit Cloud, just change the voice name after the colon in your [agent code](https://github.com/livekit-examples/voice-agent-hackathon/blob/main/src/agent.py):

```python
session = AgentSession(
    tts="rime/arcana:andromeda"
)
```

Refer to the [Rime voices list](https://docs.rime.ai/api-reference/voices) for more information.

#### Rime plugin

To use your own Rime account, or access additional features, use the Rime plugin:

```shell
uv add livekit-agents[rime]
```

```python
from livekit.plugins import rime

session = AgentSession(
    tts=rime.TTS(model="arcana", speaker="andromeda")
)
```

Refer to the [plugin documentation](https://docs.livekit.io/agents/integrations/tts/rime/) for more information.


## Other large language models

Refer to the [source code](https://github.com/livekit/agents/blob/main/livekit-agents/livekit/agents/inference/llm.py) for available models (LiveKit Inference docs are coming soon).

```python
session = AgentSession(
    llm="azure/gpt-4o-mini"
)
```

Or, use an [LLM plugin](https://docs.livekit.io/agents/integrations/llm/) for a wider range of models and more configuration options.
