"""
Configuration management module for loading and accessing application settings.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """
    Manages application configuration from config.json file.
    Provides type-safe access to configuration values with defaults.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager and load config file.
        
        Args:
            config_path: Path to configuration JSON file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from JSON file.
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key with optional default.
        Supports nested keys using dot notation (e.g., "ollama.model").
        
        Args:
            key: Configuration key (supports dot notation for nested values)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_llm_provider(self) -> str:
        """
        Get the configured LLM provider.
        
        Returns:
            LLM provider name ("ollama" or "openai")
        """
        return self.get("llm_provider", "ollama").lower()
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """
        Get Ollama configuration.
        
        Returns:
            Dictionary with Ollama settings
        """
        return {
            "base_url": self.get("ollama.base_url", "http://localhost:11434"),
            "model": self.get("ollama.model", "deepseek-r1:7b"),
            "timeout": self.get("ollama.timeout", 120)
        }
    
    def get_openai_config(self) -> Dict[str, Any]:
        """
        Get OpenAI configuration.
        
        Returns:
            Dictionary with OpenAI settings
        """
        # Support environment variable override for API key
        api_key = os.getenv("OPENAI_API_KEY") or self.get("openai.api_key", "")
        
        return {
            "api_key": api_key,
            "model": self.get("openai.model", "gpt-4o-mini"),
            "organization": self.get("openai.organization")
        }
    
    def get_generation_config(self) -> Dict[str, Any]:
        """
        Get text generation parameters.
        
        Returns:
            Dictionary with generation settings
        """
        return {
            "temperature": self.get("generation.temperature", 0.7),
            "max_tokens": self.get("generation.max_tokens", 2000),
            "top_p": self.get("generation.top_p", 0.9)
        }
    
    def get_document_config(self) -> Dict[str, Any]:
        """
        Get document processing configuration.
        
        Returns:
            Dictionary with document settings
        """
        return {
            "section_heading_styles": self.get(
                "document.section_heading_styles",
                ["Heading 1", "Heading 2", "Heading 3"]
            ),
            "placeholder_pattern": self.get(
                "document.placeholder_pattern",
                "{{SECTION_CONTENT}}"
            )
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Dictionary with logging settings
        """
        return {
            "level": self.get("logging.level", "INFO"),
            "rotation_hours": self.get("logging.rotation_hours", 1),
            "retention_days": self.get("logging.retention_days", 1)
        }
    
    def reload(self) -> None:
        """
        Reload configuration from file.
        Useful if config file has been modified.
        """
        self._load_config()


# Global config instance
_config_instance: Optional[ConfigManager] = None


def get_config(config_path: str = "config.json") -> ConfigManager:
    """
    Get or create the global configuration manager instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ConfigManager instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ConfigManager(config_path)
    
    return _config_instance