#!/usr/bin/env python3
"""Client to send requests to transcription daemon."""
import sys
import json
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: ./transcribe_client.py <audio_file> [--diarise] [--beam-size N]")
    sys.exit(1)

request = {
    "audio_file": str(Path(sys.argv[1]).absolute()),
    "diarise": "--diarise" in sys.argv,
}

if "--beam-size" in sys.argv:
    idx = sys.argv.index("--beam-size")
    request["beam_size"] = int(sys.argv[idx + 1])

print(json.dumps(request))
