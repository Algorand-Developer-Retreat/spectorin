#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# API Keys and Tokens" > .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "HUGGINGFACE_API_TOKEN=your_huggingface_token_here" >> .env
    echo "Please update the .env file with your actual API keys"
    exit 1
fi

# Source the .env file
source .env

# Validate environment variables
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "Error: OPENAI_API_KEY is not set or is using default value"
    exit 1
fi

if [ -z "$HUGGINGFACE_API_TOKEN" ] || [ "$HUGGINGFACE_API_TOKEN" = "your_huggingface_token_here" ]; then
    echo "Error: HUGGINGFACE_API_TOKEN is not set or is using default value"
    exit 1
fi

# Export the variables
export OPENAI_API_KEY
export HUGGINGFACE_API_TOKEN

# Print status
echo "Environment variables set up successfully"
echo "OpenAI API key is set"
echo "HuggingFace API token is set" 