import os
import logging
from core.ai_agents.ollama_agent import OllamaAgent
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_contract(file_path: str, language: str):
    """Analyze a single contract file"""
    logger.info(f"\nAnalyzing {file_path}...")
    
    # Read the contract file
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Initialize the Ollama agent
    agent = OllamaAgent(memory_efficient=False)
    
    # Get recommendations
    recommendations = agent.generate_recommendations(code, language, [])
    
    # Print results
    logger.info(f"\nAnalysis for {file_path}:")
    logger.info("=" * 80)
    for i, rec in enumerate(recommendations, 1):
        logger.info(f"{i}. {rec}")
    logger.info("=" * 80)

def main():
    # Get the sample contracts directory
    sample_dir = Path("sample_contracts")
    
    # Define language mappings
    language_map = {
        ".sol": "Solidity",
        ".rs": "Rust",
        ".move": "Move",
        ".py": "Python"
    }
    
    # Analyze each contract
    for file in sample_dir.glob("vulnerable.*"):
        language = language_map.get(file.suffix, "Unknown")
        analyze_contract(str(file), language)

if __name__ == "__main__":
    main() 