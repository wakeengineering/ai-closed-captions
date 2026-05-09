#!/bin/bash
# Activate virtual environment and configure library path

export HF_HOME=/mnt/i/python/cache/models/huggingface       # Hugging Face models
export TORCH_HOME=/mnt/i/python/cache/models/torch_home     # PyTorch models
export PIP_CACHE_DIR=/mnt/i/python/cache/pip   # pip packages

# Source the standard venv activation
source "${1:-venv_fw}/bin/activate"

#python transcribe_faster_whisper.py "/mnt/i/python/ai-closed-captions/test_files/Kill la Kill Official English Dubbed Trailer.wav" --compute-type float32 --beam-size 5 --vad-filter --word-timestamps
#python transcribe_faster_whisper.py "/mnt/h/Anime/The Apothecary Diaries/Season 2/Spice_and_Wolf_-_Merchant_Meets_the_Wise_Wolf_-_S01E01.mkv" --diarise --model "distil-large-v3" --compute-type float32 --beam-size 8 --extract-subtitle "Signs" --gemini-context "Spice and Wolf Remake" --vad-filter --no-cleanup #--debug
#python transcribe_faster_whisper.py "/mnt/h/Anime/The Apothecary Diaries/Season 2/" --use-dubtitle "Dub" --extract-subtitle "Signs"
python transcribe_faster_whisper.py "/mnt/h/Anime/My Hero Academia Vigilantes/Season_1" --diarise --model "large-v3-turbo" --compute-type float32 --beam-size 8 --extract-subtitle "Signs" --gemini-context "My Hero Academia Vigilantes" --vad-filter --no-cleanup #--debug