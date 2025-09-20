<!--
  AaiMinder — README
  Tip: put a wide hero image at: assets/banner_aaiminder.png  (1600x600+)
-->

<h1 align="center">📝 AaiMinder — Voice To-Do & Reminder Agent</h1>

<p align="center">
  <em>Voice-controlled to-do assistant powered by AssemblyAI (STT) + Rime (TTS) on LiveKit Agents.</em>
</p>

<p align="center">
  <img src="assets/banner_aaiminder.png<img width="391" height="456" alt="image" src="https://github.com/user-attachments/assets/08b9ea29-e07c-4f02-bad8-78b8bda8ff49" />


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

## 🧭 Table of Contents

1. [Features](#-features)  
2. [Architecture](#-architecture)  
3. [Quickstart](#-quickstart)  
   - [Clone](#1-clone)  
   - [Install](#2-install)  
   - [Configure](#3-configure)  
   - [Run](#4-run)  
4. [Usage](#-usage)  
5. [Project Structure](#-project-structure)  
6. [Flutter UI (Optional)](#-flutter-ui-optional)  
7. [Demo Script](#-demo-script)  
8. [Troubleshooting](#-troubleshooting)  
9. [Author](#-author)

---

## ✨ Features

- 🎤 **Talk naturally**: add tasks, read tasks, mark tasks done  
- ⚡ **Low-latency**: real-time STT + TTS for snappy conversations  
- 🧠 **Simple & private**: local JSON store (`tasks.json`)  
- 🧩 **Extensible**: add reminders, due dates, or a Google Sheet later

---

## 🏗 Architecture

- 🧩 **LiveKit Agents** → real-time voice agent runtime  
- 🗣 **AssemblyAI** → streaming speech-to-text (STT)  
- 🔊 **Rime** → instant text-to-speech (TTS)  
- 📂 **Local store** → `tasks.json` (no DB)

```text
Mic → LiveKit Room → AssemblyAI (STT) → Agent Tools (add/list/complete) → tasks.json → Rime (TTS) → Speaker
```

## 🚀 Quickstart

🛠 Prereqs: LiveKit Cloud project (URL, Key, Secret), AssemblyAI API key, Rime API key, Python 3.10+, uv package manager.

### 1) Clone
```
git clone https://github.com/<your-username>/AaiMinder-voice-to-do-agent-AssemblyAI-Rime-LiveKit.git
cd AaiMinder-voice-to-do-agent-AssemblyAI-Rime-LiveKit
```

### 2) Install
```
uv sync
uv pip install -U livekit-agents
uv add "livekit-agents[assemblyai]~=1.2" "livekit-agents[rime]~=1.2"
```

### 3) Configure
Create .env.local in the project root:
```
LIVEKIT_URL=wss://<your-project>.livekit.cloud
LIVEKIT_API_KEY=<your_livekit_api_key>
LIVEKIT_API_SECRET=<your_livekit_api_secret>

ASSEMBLYAI_API_KEY=<your_assemblyai_key>
RIME_API_KEY=<your_rime_key>
```

### 4) Run
Create .env.local in the project root:
```
uv run python src/agent.py download-files
uv run python src/agent.py dev
```

### 🎙 Usage
```text
Say: "add prepare slides" 
→ AaiMinder: "Added prepare slides."

Say: "read my tasks" 
→ AaiMinder: "You have 1 task: prepare slides."

Say: "mark prepare slides done" 
→ AaiMinder: "Marked prepare slides done."
```
🗂 Tasks persist in tasks.json (git-ignore recommended).

## 🗂 Project Structure
```text
src/
  agent.py           # voice pipeline + tools (AssemblyAI STT, Rime TTS)
  skills/
    todo.py          # tiny JSON-backed task store

tasks.json           # created on first run
.env.local           # secrets (do not commit)
assets/
  banner_aaiminder.png  # hero image for the README
README.md
```
### 📱 Flutter UI (Optional)

Want a pretty app with a Connect & Talk button and mic status?
**Clone LiveKit’s Flutter starter:**
```
git clone https://github.com/livekit-examples/agent-starter-flutter
cd agent-starter-flutter
flutter pub get
flutter run  # macOS, iOS, Android, or web
```

#### **Use the LiveKit Sandbox for tokens:**

# create a sandbox token server
```
lk sandbox create
# (or) wire your own token server in lib/services/token_service.dart
```

Keep your Python agent running.
The Flutter app joins the same room and streams your mic to the agent.


