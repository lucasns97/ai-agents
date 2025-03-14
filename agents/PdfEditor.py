from smolagents import ToolCallingAgent, OpenAIServerModel
from utils.conts import OPENAI_API_KEY
from agents.tools.edit_pdf import MergePDFTool, SplitPDFTool, RotatePDFTool, WatermarkPDFTool, AddPasswordToPDFTool



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
        tools=[
            MergePDFTool(),
            SplitPDFTool(),
            RotatePDFTool(),
            WatermarkPDFTool(),
            AddPasswordToPDFTool()
        ],
        model=model,
        max_steps=20,
        verbosity_level=2,
        name="PdfEditor",
        description=(
            "Edits PDF files such as merging, splitting, "
            "rotating, watermarking, and adding password protection."
        )
    )
    return agent
