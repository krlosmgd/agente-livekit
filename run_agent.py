import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import deepgram, elevenlabs, openai, silero

# Load configuration from config.json (next to this script)
CONFIG_PATH = Path(__file__).parent / "config.json"

def _load_config(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        # Non-fatal: fall back to defaults below
        print(f"Warning: could not load config.json at {path}: {e}")
        return {}

_CONFIG = _load_config(CONFIG_PATH)

# The Agent's instruction text is taken from config.json key `system_prompt`.
# If it's missing, fall back to a simple default instruction.
AGENT_INSTRUCTIONS = _CONFIG.get(
    "system_prompt",
    "You are a friendly voice assistant built by LiveKit.",
)

# Speech-to-text language (e.g. "es" or "es-CO"). Can be overridden in config.json
# Allow environment variable override (e.g. export STT_LANGUAGE=es-CO) before falling back to config.json or default
STT_LANGUAGE = os.getenv("STT_LANGUAGE") or _CONFIG.get("stt_language", "es")

@function_tool
async def lookup_weather(
    context: RunContext,
    location: str,
):
    """Used to look up weather information."""

    return {"weather": "sunny", "temperature": 70}


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions=AGENT_INSTRUCTIONS,
        tools=[lookup_weather],
    )
    session = AgentSession(
        vad=silero.VAD.load(),
        # any combination of STT, LLM, TTS, or realtime API can be used
        # Pass the desired transcription language to the STT plugin. Default is Spanish ("es").
        stt=deepgram.STT(model="nova-3", language=STT_LANGUAGE),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=elevenlabs.TTS(),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="greet the user and ask about their day")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))