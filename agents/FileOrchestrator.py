from smolagents import CodeAgent, OpenAIServerModel
from utils.conts import OPENAI_API_KEY
from agents import FileConverter, FileOrganizer, PdfEditor, ImageCreator


def initialize_model():
    """Initialize and return the Hugging Face model."""
    
    # Initialize model with specific configuration
    return OpenAIServerModel("gpt-4o", max_tokens=8096, api_key=OPENAI_API_KEY)


def get_agent():
    """Create and return a configured CodeAgent.
    
    Returns:
        CodeAgent: An initialized agent with the specified configuration.
    """
    model = initialize_model()
    
    # Instantiate the agent with defined parameters
    agent = CodeAgent(
        model=model,
        tools=[],
        managed_agents=[
            FileConverter.get_agent(),
            FileOrganizer.get_agent(),
            PdfEditor.get_agent(),
            ImageCreator.get_agent()
        ],
        additional_authorized_imports=["os", "shutil"],
        planning_interval=5,
        verbosity_level=2,
        max_steps=15,
        name="FileOrchestrator",
        description="Orchestrates file conversion and organization agents."
    )
    return agent
