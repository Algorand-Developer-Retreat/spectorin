import os
import logging
from core.ai_agents.llm_providers import LLMProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_llm_providers():
    """Test all available LLM providers"""
    logger.info("Initializing LLM providers...")
    provider = LLMProvider()
    
    # Get provider status
    status = provider.get_provider_status()
    logger.info("Provider status:")
    for name, is_available in status.items():
        logger.info(f"{name}: {'Available' if is_available else 'Not available'}")
    
    # Test each available provider
    for provider_name, llm in provider.providers:
        try:
            logger.info(f"\nTesting {provider_name}...")
            response = llm.invoke("What is 2+2?")
            logger.info(f"Response from {provider_name}: {response}")
        except Exception as e:
            logger.error(f"Error testing {provider_name}: {str(e)}")

if __name__ == "__main__":
    # Check if environment variables are set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY is not set")
    if not os.getenv("HUGGINGFACE_API_TOKEN"):
        logger.error("HUGGINGFACE_API_TOKEN is not set")
    
    test_llm_providers() 