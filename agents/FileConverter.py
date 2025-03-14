from smolagents import ToolCallingAgent, OpenAIServerModel
from utils.conts import  OPENAI_API_KEY
from agents.tools.convert import File2DocumentTool, ImageFormatConverterTool, AudioFormatConverterTool, VideoFormatConverterTool


def initialize_model():
    """Initialize and return the Hugging Face model."""
    
    # Initialize model with specific configuration
    return OpenAIServerModel("gpt-4o-mini", max_tokens=2048, api_key=OPENAI_API_KEY)


def get_agent():
    """Create and return a configured ToolCallingAgent.
    
    Returns:
        ToolCallingAgent: An initialized agent with the specified configuration.
    """
    model = initialize_model()
    
    # Instantiate the agent with defined parameters
    agent = ToolCallingAgent(
        tools=[File2DocumentTool(), ImageFormatConverterTool(), AudioFormatConverterTool(), VideoFormatConverterTool()],
        model=model,
        max_steps=20,
        verbosity_level=2,
        name="FileConverter",
        description="Converts files from one format to another."
    )
    return agent
