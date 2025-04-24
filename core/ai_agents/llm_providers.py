from langchain_community.llms import Ollama
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models import ChatOpenAI
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(self):
        self.providers = []
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize LLM providers in priority order"""
        # Try Ollama first
        try:
            ollama = Ollama(
                model="phi3:mini",
                timeout=30,
                temperature=0.3,
                num_ctx=4096,
                num_thread=4,
                stop=["</s>", "Human:", "Assistant:"]
            )
            self.providers.append(("ollama", ollama))
            logger.info("Ollama provider initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama: {str(e)}")

        # Try HuggingFace second
        try:
            hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            if hf_token:
                logger.info(f"HuggingFace token found: {hf_token[:4]}...{hf_token[-4:]}")
                hf = HuggingFaceEndpoint(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
                    task="text-generation",
                    temperature=0.7,
                    model_kwargs={"max_length": 2048},
                    huggingfacehub_api_token=hf_token
                )
                self.providers.append(("huggingface", hf))
                logger.info("HuggingFace provider initialized successfully")
            else:
                logger.warning("HuggingFace API token not found")
        except Exception as e:
            logger.warning(f"Failed to initialize HuggingFace: {str(e)}")

        # Try OpenAI last
        try:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                openai = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=2048
                )
                self.providers.append(("openai", openai))
                logger.info("OpenAI provider initialized successfully")
            else:
                logger.warning("OpenAI API key not found")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI: {str(e)}")

    def get_available_provider(self) -> Optional[tuple[str, Any]]:
        """Get the first available provider"""
        for provider_name, provider in self.providers:
            try:
                # Test the provider with a simple prompt
                provider.invoke("test")
                return provider_name, provider
            except Exception as e:
                logger.warning(f"Provider {provider_name} failed: {str(e)}")
                continue
        return None

    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all providers"""
        status = {}
        for provider_name, provider in self.providers:
            try:
                provider.invoke("test")
                status[provider_name] = True
            except Exception:
                status[provider_name] = False
        return status 