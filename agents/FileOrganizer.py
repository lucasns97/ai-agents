from smolagents import CodeAgent, OpenAIServerModel
from utils.conts import OPENAI_API_KEY
from agents.tools.system import RenameFileTool, DeleteFileTool, CopyFileTool


def initialize_model():
    """Initialize and return the Hugging Face model."""
    
    # Initialize model with specific configuration
    return OpenAIServerModel("gpt-4o-mini", max_tokens=2048, api_key=OPENAI_API_KEY)


def get_agent():
    """Create and return a configured CodeAgent.
    
    Returns:
        CodeAgent: An initialized agent with the specified configuration.
    """
    model = initialize_model()
    
    # Instantiate the agent with defined parameters
    agent = CodeAgent(
        tools=[RenameFileTool(), DeleteFileTool(), CopyFileTool()],
        model=model,
        max_steps=20,
        verbosity_level=2,
        additional_authorized_imports=["os", "shutil"],
        name="FileOrganizer",
        description="Organizes and manages files in the local file system."
    )
    return agent
