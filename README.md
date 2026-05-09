# AI Closed Captions

AI-driven English closed captions generator, optimized for RTX 5080 hardware. This project provides tools for transcribing audio from video files into English subtitles, with a focus on anime content where matching English dubs are often unavailable.

## Overview

This repository contains experimental scripts for generating closed captions using AI transcription models. The primary working implementation is `transcribe_faster_whisper.sh`, a wrapper script that orchestrates the underlying Python components for transcription.

An earlier attempt using WhisperX was aborted due to compatibility and performance issues.

## Features

The main pipeline (`transcribe_faster_whisper.sh`) includes the following capabilities:

- **API Context Integration**: Leverages external APIs to gather contextual information about the video content, improving transcription accuracy.
- **Sign/Song Merging**: Automatically detects and merges signs, songs, and other non-dialogue elements into the subtitle track.
- **Existing Subtitle Detection and Merging**: Identifies pre-existing closed caption tracks in the video file and merges them with the new AI-generated subtitles for comprehensive coverage.

## Usage

**Note**: This project is highly experimental and requires significant manual intervention. It is not a fully automated solution.

1. Ensure you have the necessary dependencies installed (see `requirements_fw.txt` for Python packages).
2. Prepare your video file and gather context:
   - Know the expected list of existing subtitle tracks.
   - Manually input the proper name of the video, TV show, or movie to fetch relevant context.
3. Run the primary script:
   ```
   ./transcribe_faster_whisper.sh [video_file] [options]
   ```
   Customize prompts and context as needed for optimal results.

## Caveats and Limitations

- **Experimental Status**: This is an ongoing, incomplete project. Results vary greatly depending on the video file.
- **Manual Knowledge Required**: Success depends on your familiarity with the target video file, including its subtitle tracks and content details.
- **Context Prompting**: Requires manual input of accurate video names and contextual information to improve transcription quality.
- **Anime Focus**: Primarily tested and used for anime content, which is notorious for lacking synchronized English subtitles for dubs.
- **Hardware Specific**: Optimized for RTX 5080; performance may vary on other systems.

Use at your own risk, and expect to iterate on results manually.

## Requirements

- Python 3.x
- Dependencies listed in `requirements_fw.txt`
- RTX 5080 GPU (recommended)
- FFmpeg or similar for video processing

## Contributing

This is a personal project, but feel free to fork and experiment. Pull requests for improvements are welcome, though the project is not actively maintained.

## License

[Add your preferred license here, e.g., MIT]
