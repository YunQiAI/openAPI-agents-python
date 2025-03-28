import asyncio
import sys
import os

# Add project root to Python path to ensure src package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from openai.types.responses import ResponseTextDeltaEvent, ResponseContentPartDoneEvent
from src.agents import Agent, RawResponsesStreamEvent, Runner
from src.agents.model_settings import ModelSettings
from src.agents.run import RunConfig
from src.agents.models.azure_openai_provider import AzureOpenAIProvider

"""
This example demonstrates how to stream text responses from Azure OpenAI.
Text is printed as it's generated by the model, character by character.
"""

async def main():
    # Create run configuration
    run_config = RunConfig()
    
    # Create provider directly, it will automatically read configuration from environment variables
    run_config.model_provider = AzureOpenAIProvider()
    
    # Create Azure OpenAI model settings
    azure_settings = ModelSettings(
        provider="azure_openai",  # Specify Azure OpenAI as the provider
        temperature=0.7  # Optional: control creativity
    )
    
    agent = Agent(
        name="Streaming Agent",
        instructions="You are a helpful agent that provides information about astronomy.",
        model_settings=azure_settings,
    )
    
    # Get input from user
    user_input = input("Ask a question about astronomy: ")
    
    print("\nGenerating response...\n")
    
    # Run the agent with streaming enabled
    result = Runner.run_streamed(agent, user_input, run_config=run_config)
    
    # Process the stream events
    async for event in result.stream_events():
        # We're only interested in raw response events that contain text deltas
        if not isinstance(event, RawResponsesStreamEvent):
            continue
        
        data = event.data
        if isinstance(data, ResponseTextDeltaEvent):
            # Print the delta text without a newline
            print(data.delta, end="", flush=True)
        elif isinstance(data, ResponseContentPartDoneEvent):
            # Add a newline when content part is done
            print("\n")


if __name__ == "__main__":
    # Print usage instructions
    print("Azure OpenAI Streaming Text Example")
    print("=================================")
    print("This example requires Azure OpenAI credentials.")
    print("Make sure you have set these environment variables:")
    print("- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key")
    print("- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL")
    print("- AZURE_OPENAI_API_VERSION: (Optional) API version")
    print("- AZURE_OPENAI_DEPLOYMENT: (Optional) Deployment name")
    print()
    
    # Run the main function
    asyncio.run(main())
