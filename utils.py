"""Utility classes for logging and timing."""
import time
import configparser
import logging
import re
from pathlib import Path
from datetime import datetime


def load_config() -> configparser.ConfigParser:
	"""Load tokens from private/ai-closed-captions.conf"""
	config = configparser.ConfigParser()
	config_path = Path(__file__).parent / "private" / "ai-closed-captions.conf"
	if config_path.exists():
		config.read(config_path)
	return config


class Logger:
	"""Simple logger for basic and debug-level messages with file logging support."""
	def __init__(self, debug: bool = False):
		self.debug_enabled = debug
		# Create underlying Python logger
		self.logger = logging.getLogger('transcribe')
		self.logger.setLevel(logging.DEBUG)
		
		# Add console handler if not already present
		if not self.logger.handlers:
			console_handler = logging.StreamHandler()
			console_handler.setLevel(logging.DEBUG)
			console_handler.setFormatter(logging.Formatter('%(message)s'))
			self.logger.addHandler(console_handler)
	
	def basic(self, message: str) -> None:
		"""Always log a message at INFO level."""
		self.logger.info(message)
	
	def debug(self, message: str) -> None:
		"""Log message at DEBUG level only if debug mode is enabled."""
		if self.debug_enabled:
			self.logger.debug(message)


class Timer:
	"""Simple timer to track elapsed time and report checkpoints."""
	def __init__(self):
		self.start_time = time.time()
		self.last_checkpoint = self.start_time
	
	def elapsed(self) -> float:
		"""Get total elapsed time since script start in seconds."""
		return time.time() - self.start_time
	
	def checkpoint(self, label: str = "") -> float:
		"""Log elapsed time and return delta since last checkpoint."""
		current = time.time()
		delta = current - self.last_checkpoint
		total = current - self.start_time
		if label:
			print(f"{label}: {delta:.2f}s (total: {total:.2f}s)")
		self.last_checkpoint = current
		return delta


# ============================================================================
# FILE LOGGING UTILITIES
# ============================================================================

def sanitize_filename(filename: str) -> str:
	"""Remove/replace special characters from filename for use as log file.
	
	Keeps alphanumerics, dots, hyphens, underscores. Replaces spaces with underscores.
	"""
	# Replace spaces with underscores
	name = filename.replace(' ', '_')
	# Remove file extension if present
	name = name.rsplit('.', 1)[0] if '.' in name else name
	# Keep only alphanumerics, dots, hyphens, underscores
	name = re.sub(r'[^a-zA-Z0-9._-]', '', name)
	# Remove consecutive underscores
	name = re.sub(r'_+', '_', name)
	return name.strip('_')


def setup_file_logging(log_dir: Path | None) -> tuple[logging.FileHandler | None, logging.FileHandler | None]:
	"""Setup general and video-specific file handlers if log_dir is set.
	
	Returns:
		Tuple of (general_handler, video_handler) or (None, None) if log_dir not set
	"""
	if not log_dir:
		return None, None
	
	try:
		log_dir = Path(log_dir)
		log_dir.mkdir(parents=True, exist_ok=True)
		
		# Create formatter
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		
		# General log file (dated with time for per-run rotation)
		run_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
		general_log_path = log_dir / f"general_{run_timestamp}.log"
		general_handler = logging.FileHandler(general_log_path, encoding='utf-8')
		general_handler.setFormatter(formatter)
		general_handler.setLevel(logging.DEBUG)
		
		# Video handler will be created per-video, start as None
		video_handler = None
		
		return general_handler, video_handler
	
	except Exception as e:
		print(f"Error setting up file logging: {e}")
		return None, None


def add_handler_to_logger(logger: Logger, handler: logging.FileHandler) -> None:
	"""Add a file handler to the logger's underlying logging object."""
	if handler:
		logger.logger.addHandler(handler)


def remove_handler_from_logger(logger: Logger, handler: logging.FileHandler) -> None:
	"""Remove a file handler from the logger."""
	if handler:
		logger.logger.removeHandler(handler)
		handler.close()
