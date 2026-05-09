#!/bin/bash
# Activate virtual environment and configure library path

# Source the standard venv activation
source "${1:-venv}/bin/activate"

# Store the old LD_LIBRARY_PATH for restoration on deactivate
# export _OLD_LD_LIBRARY_PATH="${LD_LIBRARY_PATH}"

# # Add the venv's lib directory to LD_LIBRARY_PATH
# # The conditional expansion handles the case where LD_LIBRARY_PATH is unset
# export LD_LIBRARY_PATH="${VIRTUAL_ENV}/lib:\
# /usr/local/cuda-12.8/lib64:\
# /usr/lib/x86_64-linux-gnu:\
# ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

# echo "Virtual environment activated: $VIRTUAL_ENV"
# echo "LD_LIBRARY_PATH updated to include: $VIRTUAL_ENV/lib"

python transcribe_whisperx.py "/mnt/i/python/ai-closed-captions/test_files/Kill la Kill Official English Dubbed Trailer.mp3" --compute-type float32 --beam-size 5 --vad-filter --word-timestamps