# M.A.N.S.A.

**Modular Agent Network for Software & Academics**

M.A.N.S.A. is a modular personal AI assistant built in Python to support academics, software development, and game development.

The project is designed around a modular architecture rather than a single monolithic assistant. User interaction, command routing, specialized agents, AI inference, and persistent memory are separated into independent components that can evolve over time.

M.A.N.S.A. currently runs locally using Ollama and Qwen, allowing AI features to operate without requiring a paid cloud API.

## Current Version

**v0.1.0**

Completed development milestones:

- Mark 0: Boot Sequence
- Mark I: Core Assistant
- Mark II: AI Brain
- Mark III: Persistent Memory

## Architecture

M.A.N.S.A. is divided into several major components:

```text
                         ┌── Academic Agent
                         │
                         ├── Development Agent
User → C.H.A.T. → S.O.U.L. ├── Game Development Agent
                         │
                         ├── System Tools
                         │
                         ├── Memory System → SQLite
                         │
                         └── AI Provider
                                ↓
                          LocalProvider
                                ↓
                             Ollama
                                ↓
                           Qwen3:4b
```

### C.H.A.T.

**Central Hub for Agents & Tools**

C.H.A.T. is the conversational interface of M.A.N.S.A. It receives user input, manages the active session, displays responses, and handles universal commands such as shutdown.

### S.O.U.L.

**Software Orchestration & Understanding Layer**

S.O.U.L. acts as M.A.N.S.A.'s routing and orchestration layer. It determines whether input should be handled by a system command, specialized agent, memory operation, or the AI provider.

### Specialized Agents

M.A.N.S.A. currently contains dedicated modes for:

- Academic tasks
- Software development
- Game development

These agents currently provide the architectural foundation for more advanced domain-specific tools planned for future versions.

### AI Provider

M.A.N.S.A. uses a provider abstraction so that the underlying AI model is not permanently tied to the rest of the application.

The current local provider connects to:

- Ollama
- Qwen3:4b

This architecture allows other local or cloud AI providers to be added later without redesigning the entire assistant.

## Persistent Memory

M.A.N.S.A. uses SQLite for local persistent memory.

Unlike conversation history, persistent memories survive application restarts.

Current memory features include:

- Create memories
- Read stored memories
- Update memories
- Delete memories
- Categorize memories
- Store profile information
- Update the user's preferred name
- Search memories
- Retrieve relevant memories for AI requests

Supported memory categories currently include:

- `general`
- `academic`
- `project`
- `preference`
- `development`
- `game_dev`

## Memory Retrieval

M.A.N.S.A. uses query-dependent keyword retrieval to determine which persistent memories should be provided to the AI.

The current retrieval pipeline is:

```text
User Query
    ↓
Keyword Extraction
    ↓
Stop-Word Filtering
    ↓
Memory Comparison
    ↓
Relevance Scoring
    ↓
Top Relevant Memories
    ↓
AI Context
    ↓
Qwen
```

This prevents every stored memory from being sent to the model for every request.

The current system uses keyword overlap rather than embedding-based semantic retrieval.

## Commands

### System

```text
help
status
version
about
history
mode
exit
quit
shutdown
```

### Profile

```text
call me <name>
```

### Memory

```text
remember <text>
remember <category> <text>
memories
search memories <text>
update <memory id> <new text>
forget <memory id>
```

### Modes

M.A.N.S.A. supports aliases for switching between specialized modes.

Examples:

```text
academic
study
homework

development
develop
coding

game
gaming
unity
```

Use:

```text
back
```

to leave the current mode.

## Technology Stack

- Python
- SQLite
- Ollama
- Qwen3:4b
- Git
- GitHub

## Project Structure

```text
MANSA/
├── main.py
├── chat.py
├── config.py
├── logger.py
├── core/
│   ├── __init__.py
│   ├── soul.py
│   ├── session.py
│   ├── system.py
│   └── help.py
├── agents/
│   ├── __init__.py
│   ├── academic.py
│   ├── developer.py
│   └── game_dev.py
├── ai/
│   ├── __init__.py
│   ├── provider.py
│   └── local_provider.py
├── memory/
│   ├── __init__.py
│   └── database.py
├── data/
│   └── mansa.db
└── README.md
```

## Running M.A.N.S.A.

M.A.N.S.A. currently requires Python and Ollama.

Start the Ollama service if it is not already running:

```bash
ollama serve
```

Make sure the current local model is available:

```bash
ollama pull qwen3:4b
```

From the M.A.N.S.A. project directory, activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python main.py
```

When finished, the currently loaded model can be released with:

```bash
ollama stop qwen3:4b
```

## Development Roadmap

### Completed

- **Mark 0: Boot Sequence**
- **Mark I: Core Assistant**
- **Mark II: AI Brain**
- **Mark III: Persistent Memory**

### Planned

- **Mark IV: Academic Intelligence**
- **Mark V: Development Intelligence**
- **Mark VI: Game Development Intelligence**
- **Mark VII: Voice**
- **Mark VIII: External Tools**
- **Mark IX: M.A.E.S.T.R.O. / Multi-Agent Orchestration**
- **Mark X: Proactive Assistant**

Future development may include semantic memory retrieval, additional AI providers, external tool integrations, voice interaction, and more advanced multi-agent orchestration.

## Project Goals

M.A.N.S.A. began as both a personal productivity tool and a software engineering learning project.

Its long-term goal is to develop into a modular assistant capable of supporting academic work, software projects, game development, tool usage, persistent context, and eventually proactive multi-agent workflows while maintaining clear separation between system components.

## Status

M.A.N.S.A. is under active development.

**Current release: v0.1.0**