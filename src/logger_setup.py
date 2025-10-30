"""
Logging configuration module with automatic rotation and cleanup.
Creates timestamped log files, rotates hourly, and removes old logs.
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class TimedRotatingLogger:
    """
    Manages application logging with hourly rotation and automatic cleanup.
    Log files are named with timestamps and stored in the logs directory.
    """
    
    def __init__(
        self,
        log_dir: str = "logs",
        retention_days: int = 1,
        rotation_hours: int = 1,
        level: str = "INFO"
    ):
        """
        Initialize the logging system.
        
        Args:
            log_dir: Directory to store log files
            retention_days: Number of days to keep log files
            rotation_hours: Hours between log file rotations
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.retention_days = retention_days
        self.rotation_hours = rotation_hours
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.logger: Optional[logging.Logger] = None
        self.current_log_file: Optional[Path] = None
        self.last_rotation: Optional[datetime] = None
        
        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up old logs on initialization
        self._cleanup_old_logs()
        
        # Initialize logger
        self._setup_logger()
    
    def _generate_log_filename(self) -> Path:
        """
        Generate a timestamped log filename.
        
        Returns:
            Path object for the new log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.log_dir / f"app_{timestamp}.log"
    
    def _cleanup_old_logs(self) -> None:
        """
        Remove log files older than retention_days.
        """
        if not self.log_dir.exists():
            return
        
        cutoff_time = datetime.now() - timedelta(days=self.retention_days)
        removed_count = 0
        
        for log_file in self.log_dir.glob("app_*.log"):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_time:
                    log_file.unlink()
                    removed_count += 1
            except (OSError, ValueError) as e:
                print(f"Error removing old log file {log_file}: {e}")
        
        if removed_count > 0:
            print(f"Cleaned up {removed_count} old log file(s)")
    
    def _setup_logger(self) -> None:
        """
        Set up the logger with file and console handlers.
        """
        # Create new log file
        self.current_log_file = self._generate_log_filename()
        self.last_rotation = datetime.now()
        
        # Get or create logger
        self.logger = logging.getLogger("word_llm_generator")
        self.logger.setLevel(self.level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.current_log_file, encoding="utf-8")
        file_handler.setLevel(self.level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logging initialized: {self.current_log_file}")
        self.logger.info(f"Log level: {logging.getLevelName(self.level)}")
    
    def check_rotation(self) -> None:
        """
        Check if log rotation is needed and rotate if necessary.
        """
        if self.last_rotation is None:
            return
        
        time_since_rotation = datetime.now() - self.last_rotation
        if time_since_rotation.total_seconds() >= (self.rotation_hours * 3600):
            self.logger.info("Rotating log file")
            self._setup_logger()
            self._cleanup_old_logs()
    
    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.
        
        Returns:
            Configured logger
        """
        # Check if rotation is needed
        self.check_rotation()
        return self.logger


# Global logger instance
_logger_instance: Optional[TimedRotatingLogger] = None


def setup_logging(
    log_dir: str = "logs",
    retention_days: int = 1,
    rotation_hours: int = 1,
    level: str = "INFO"
) -> logging.Logger:
    """
    Set up and return the application logger.
    
    Args:
        log_dir: Directory to store log files
        retention_days: Number of days to keep log files
        rotation_hours: Hours between log file rotations
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = TimedRotatingLogger(
            log_dir=log_dir,
            retention_days=retention_days,
            rotation_hours=rotation_hours,
            level=level
        )
    
    return _logger_instance.get_logger()


def get_logger() -> logging.Logger:
    """
    Get the application logger instance.
    
    Returns:
        Logger instance
    
    Raises:
        RuntimeError: If logger has not been set up
    """
    global _logger_instance
    
    if _logger_instance is None:
        raise RuntimeError("Logger not initialized. Call setup_logging() first.")
    
    return _logger_instance.get_logger()