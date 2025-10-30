"""
LLM client module for interacting with Ollama and OpenAI APIs.
Provides unified interface for text generation across different providers.
"""

import json
import time
from typing import Dict, List, Optional
import requests
from openai import OpenAI

from src.logger_setup import get_logger


class LLMClient:
    """
    Unified client for LLM text generation supporting Ollama and OpenAI.
    Handles API calls, retries, error handling, and token tracking.
    """
    
    def __init__(
        self,
        provider: str,
        provider_config: Dict,
        generation_config: Dict
    ):
        """
        Initialize LLM client with provider-specific configuration.
        
        Args:
            provider: LLM provider ("ollama" or "openai")
            provider_config: Provider-specific configuration
            generation_config: Text generation parameters
        """
        self.provider = provider.lower()
        self.provider_config = provider_config
        self.generation_config = generation_config
        self.logger = get_logger()
        
        # Initialize provider-specific client
        if self.provider == "openai":
            self._init_openai_client()
        elif self.provider == "ollama":
            self._init_ollama_client()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        self.logger.info(f"LLM Client initialized with provider: {self.provider}")
    
    def _init_openai_client(self) -> None:
        """
        Initialize OpenAI client.
        
        Raises:
            ValueError: If API key is missing
        """
        api_key = self.provider_config.get("api_key")
        if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
            raise ValueError("OpenAI API key not configured. Set in config.json or OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(
            api_key=api_key,
            organization=self.provider_config.get("organization")
        )
        self.model = self.provider_config.get("model", "gpt-4o-mini")
        self.logger.info(f"OpenAI client initialized with model: {self.model}")
    
    def _init_ollama_client(self) -> None:
        """
        Initialize Ollama client configuration.
        """
        self.base_url = self.provider_config.get("base_url", "http://localhost:11434")
        self.model = self.provider_config.get("model", "deepseek-r1:7b")
        self.timeout = self.provider_config.get("timeout", 120)
        self.logger.info(f"Ollama client initialized: {self.base_url}, model: {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3
    ) -> str:
        """
        Generate text using the configured LLM provider.
        
        Args:
            prompt: User prompt/message
            system_message: Optional system message for context
            temperature: Override default temperature
            max_tokens: Override default max tokens
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text content
            
        Raises:
            Exception: If generation fails after retries
        """
        # Use provided values or fall back to config
        temp = temperature if temperature is not None else self.generation_config.get("temperature", 0.7)
        tokens = max_tokens if max_tokens is not None else self.generation_config.get("max_tokens", 2000)
        
        self.logger.info(f"Generating text with {self.provider}, temp={temp}, max_tokens={tokens}")
        self.logger.debug(f"Prompt length: {len(prompt)} characters")
        
        for attempt in range(max_retries):
            try:
                if self.provider == "openai":
                    return self._generate_openai(prompt, system_message, temp, tokens)
                elif self.provider == "ollama":
                    return self._generate_ollama(prompt, system_message, temp, tokens)
            except Exception as e:
                self.logger.warning(f"Generation attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"All generation attempts failed")
                    raise
    
    def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            temperature: Temperature parameter
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        self.logger.debug(f"Calling OpenAI API with {len(messages)} messages")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=self.generation_config.get("top_p", 0.9)
        )
        
        generated_text = response.choices[0].message.content
        
        # Log token usage
        if hasattr(response, "usage"):
            usage = response.usage
            self.logger.info(
                f"OpenAI tokens - prompt: {usage.prompt_tokens}, "
                f"completion: {usage.completion_tokens}, total: {usage.total_tokens}"
            )
        
        self.logger.info(f"Generated {len(generated_text)} characters")
        return generated_text
    
    def _generate_ollama(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            temperature: Temperature parameter
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        url = f"{self.base_url}/api/chat"
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": self.generation_config.get("top_p", 0.9)
            }
        }
        
        self.logger.debug(f"Calling Ollama API at {url}")
        
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        result = response.json()
        
        generated_text = result.get("message", {}).get("content", "")
        
        # Log token usage if available
        if "prompt_eval_count" in result:
            self.logger.info(
                f"Ollama tokens - prompt: {result.get('prompt_eval_count', 0)}, "
                f"completion: {result.get('eval_count', 0)}"
            )
        
        self.logger.info(f"Generated {len(generated_text)} characters")
        return generated_text
    
    def test_connection(self) -> bool:
        """
        Test connection to the LLM provider.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.logger.info(f"Testing connection to {self.provider}...")
            test_prompt = "Hello, please respond with 'OK'."
            response = self.generate(test_prompt, max_tokens=10, max_retries=1)
            self.logger.info(f"Connection test successful: {response[:50]}")
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
        