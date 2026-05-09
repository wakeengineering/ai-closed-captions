#!/usr/bin/env python3
"""Long-running daemon that keeps models loaded for fast transcription."""
import sys
import time
import json
from pathlib import Path
from transcribe_faster_whisper import (
    WhisperModel, transcribe_full_audio, transcribe_with_diarization,
    _write_srt, TranscribedSegment
)

IDLE_TIMEOUT = 600  # 10 minutes idle = shutdown
MODEL_ID = "Systran/faster-whisper-large-v3"
COMPUTE_TYPE = "float16"

print("=== Transcription Daemon Starting ===")
print(f"Loading model: {MODEL_ID} ({COMPUTE_TYPE})")
model = WhisperModel(MODEL_ID, device="cuda", compute_type=COMPUTE_TYPE)
print("Model loaded. Ready for requests.")
print(f"Will auto-shutdown after {IDLE_TIMEOUT}s idle.\n")

last_activity = time.time()

while True:
    print("Enter JSON request (or 'exit'):", flush=True)
    try:
        line = sys.stdin.readline()
        if not line or line.strip().lower() == 'exit':
            break
        
        last_activity = time.time()
        req = json.loads(line)
        
        audio_path = Path(req['audio_file'])
        output_path = Path(req.get('output', audio_path.with_suffix('.srt')))
        beam_size = req.get('beam_size', 5)
        diarise = req.get('diarise', False)
        
        print(f"Processing: {audio_path}")
        
        if diarise:
            segments = transcribe_with_diarization(audio_path, model, beam_size)
        else:
            segments = transcribe_full_audio(
                audio_path, model, beam_size, 
                req.get('vad_filter', False),
                req.get('word_timestamps', False),
                None
            )
        
        _write_srt(segments, output_path)
        print(json.dumps({"status": "success", "output": str(output_path)}))
        
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON"}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
    
    # Check idle timeout
    if time.time() - last_activity > IDLE_TIMEOUT:
        print(f"\nIdle timeout ({IDLE_TIMEOUT}s). Shutting down.")
        break

print("=== Daemon Stopped ===")
