from smolagents import ToolCallingAgent, load_tool, OpenAIServerModel, Tool
from utils.conts import OPENAI_API_KEY
from PIL import Image
import os

class SaveImageTool(Tool):
    name = "save_image_tool"
    description = (
        "A tool for saving a PIL image to the specified path. "
        "Provide the PIL image object and the desired filename including extension. "
        "If no filename is provided, a unique filename will be generated."
    )
    inputs = {
        "image": {
            "type": "object",
            "description": "A PIL Image object to be saved.",
        },
        "filename": {
            "type": "string",
            "description": "The desired filename including extension (e.g., 'my_image.png').",
            "nullable": True
        },
        "output_dir": {
            "type": "string",
            "description": "Directory where the image should be saved. Defaults to current working directory.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, image: Image, filename: str = None, output_dir: str = None) -> str:
        """
        Saves a PIL image to the specified directory.
        
        Parameters:
            image: A PIL Image object to be saved.
            filename: Optional. The desired filename including extension (e.g., 'my_image.png').
                    If not provided, a unique filename will be generated.
            output_dir: Directory where the image should be saved. Defaults to current working directory.
            
        Returns:
            str: A message containing the full path to the saved image file.
        """
        try:
            # Check if the image is a valid PIL Image
            if not hasattr(image, "save"):
                return "Error: Provided object is not a valid PIL Image."
            
            # Generate a unique filename if none is provided
            if filename is None:
                filename = f"image_{uuid.uuid4().hex}.png"
            
            # Use the specified output directory or the current working directory
            if output_dir is None:
                output_dir = os.getcwd()
            
            # Create the output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Construct the full file path
            full_path = os.path.join(output_dir, filename)
            
            # Save the image
            image.save(full_path)
            
            return f"Image saved successfully at: {full_path}"
        except Exception as e:
            return f"Error saving image: {str(e)}"


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
    
    # Load the image generation tool
    image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)
    
    # Instantiate the agent with defined parameters
    agent = ToolCallingAgent(
        tools=[
            image_generation_tool,
            SaveImageTool()
        ],
        model=model,
        max_steps=15,
        verbosity_level=2,
        planning_interval=3,
        name="ImageCreator",
        description=(
            "Creates and saves AI-generated images based on text descriptions. "
        )
    )
    return agent


if __name__ == "__main__":
    # Test the image generation and saving
    agent = get_agent()
    result = agent.run(
        "Generate an image of a frog wearing a pig helmet and sliding over the pyramids of Egypt."
        r" Save it 'C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\.sandbox\frog.png'.",
    )
    print(result)
