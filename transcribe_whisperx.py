#!/usr/bin/env python3
"""Minimal CLI to transcribe an audio file to SRT using whisperx."""

import argparse
from pathlib import Path
import sys
import whisperx


def _format_timestamp(seconds: float) -> str:
	"""Convert float seconds to SRT timestamp (HH:MM:SS,mmm)."""

	millis = int(round(seconds * 1000))
	hours, millis = divmod(millis, 3_600_000)
	minutes, millis = divmod(millis, 60_000)
	secs, millis = divmod(millis, 1_000)
	return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def _write_srt(segments, output_path: Path) -> None:
	with output_path.open("w", encoding="utf-8") as fh:
		for idx, segment in enumerate(segments, start=1):
			start = _format_timestamp(segment.start)
			end = _format_timestamp(segment.end)
			text = segment.text.strip()
			fh.write(f"{idx}\n{start} --> {end}\n{text}\n\n")


def _write_words_json(segments, output_path: Path) -> None:
	words = []
	for seg in segments:
		if getattr(seg, "words", None):
			for w in seg.words:
				words.append(
					{
						"word": w.word,
						"start": w.start,
						"end": w.end,
						"probability": getattr(w, "probability", None),
					}
				)

	if not words:
		return

	import json
	with output_path.open("w", encoding="utf-8") as fh:
		json.dump(words, fh, ensure_ascii=False, indent=2)


def transcribe_to_srt(
	audio_path: Path,
	model_id: str,
	compute_type: str,
	beam_size: int,
	vad_filter: bool,
	word_timestamps: bool,
	words_path: Path | None,
	output_path: Path,
) -> Path:
	model = whisperx.load_model(model_id, device="cuda", compute_type=compute_type)
	audio = whisperx.load_audio(str(audio_path))
	result = model.transcribe(audio, batch_size=16)
	segments = result["segments"]

	_write_srt(segments, output_path)

	if word_timestamps and words_path:
		_write_words_json(segments, words_path)

	print(f"Detected language: {result['language']}")
	print(f"Wrote SRT: {output_path}")
	return output_path


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("audio_file", type=Path, help="Path to input audio file")
	parser.add_argument(
		"--model",
		default="Systran/faster-whisper-large-v3",
		help="Model ID to load",
	)
	parser.add_argument(
		"--compute-type",
		default="float32",
		help="Compute type (e.g., float16, float32, int8_float16)",
	)
	parser.add_argument(
		"--beam-size",
		type=int,
		default=5,
		help="Beam size for decoding",
	)
	parser.add_argument(
		"--vad-filter",
		action="store_true",
		help="Enable VAD filtering (uses Silero VAD)",
	)
	parser.add_argument(
		"--word-timestamps",
		action="store_true",
		help="Enable word-level timestamps during transcription",
	)
	parser.add_argument(
		"--words-json",
		type=Path,
		help="Optional path to write word-level timestamps JSON (requires --word-timestamps)",
	)
	parser.add_argument(
		"--output",
		type=Path,
		help="Optional output SRT path (defaults to audio filename with .srt)",
	)
	return parser.parse_args()


def main() -> None:
	# import os
	# print("All Environment Variables:")
	# print("=" * 60)

	# for key, value in sorted(os.environ.items()):
	# 	print(f"{key}={value}")
	# print("\n" + "=" * 60)
	# print("LD_LIBRARY_PATH Status:")
	# print("=" * 60)
	# sys.exit(0)

	args = parse_args()

	if not args.audio_file.exists():
		raise FileNotFoundError(f"Audio file not found: {args.audio_file}")

	output_path = args.output or args.audio_file.with_suffix(".srt")
	words_path = args.words_json if args.words_json else (
		args.audio_file.with_suffix(".words.json") if args.word_timestamps else None
	)

	transcribe_to_srt(
		audio_path=args.audio_file,
		model_id=args.model,
		compute_type=args.compute_type,
		beam_size=args.beam_size,
		vad_filter=args.vad_filter,
		word_timestamps=args.word_timestamps,
		words_path=words_path,
		output_path=output_path,
	)


if __name__ == "__main__":
	main()
