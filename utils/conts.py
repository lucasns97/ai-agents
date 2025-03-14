import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Set global constants
# API Keys
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")