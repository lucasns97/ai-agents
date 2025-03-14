#!/usr/bin/env python
"""
Main entry point for running AI agents.
This script handles initialization, user input, and execution of agent tasks.
"""

import os
import sys

# Add parent directory to path BEFORE other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import traceback
from importlib import import_module
from utils.logging import get_logger

# Get the logger instance
logger = get_logger(__name__)

# Add parent directory to path to allow importing from sibling packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def list_available_agents():
    """List all available agents in the agents directory."""
    agents_dir = os.path.dirname(os.path.abspath(__file__))
    available_agents = []
    
    for item in os.listdir(agents_dir):
        item_path = os.path.join(agents_dir, item)
        # Check if the item is a directory and contains a Python file with the same name
        if os.path.isdir(item_path) and item != "__pycache__":
            agent_file = os.path.join(item_path, f"{item}.py")
            if os.path.isfile(agent_file):
                available_agents.append(item)
    
    return available_agents


def load_agent(agent_name):
    """
    Dynamically load and initialize an agent by name.
    
    Args:
        agent_name (str): Name of the agent to load
        
    Returns:
        object: The initialized agent instance
    """
    try:
        # Import the agent module dynamically
        module_path = f"agents.{agent_name}"
        agent_module = import_module(module_path)

        logger.info(f"Loaded agent module: {module_path}")
        # Check if the module has a get_agent function
        if hasattr(agent_module, "get_agent"):
            return agent_module.get_agent()
        else:
            raise AttributeError(f"The {agent_name} module does not have a get_agent() function.")
    except ImportError as e:
        logger.info(f"Error: Could not import agent '{agent_name}'. {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"Error loading agent: {str(e)}")
        logger.info("\nDetailed error information:")
        traceback.logger.info_exc()
        sys.exit(1)


def main():
    """Main function to parse arguments and run the specified agent."""
    available_agents = list_available_agents()
    
    parser = argparse.ArgumentParser(description="Run AI agents with specific tasks.")
    parser.add_argument(
        "agent", 
        choices=available_agents,
        help="Name of the agent to run"
    )
    parser.add_argument(
        "request", 
        nargs='+',
        help="Request or task for the agent to perform"
    )
    
    args = parser.parse_args()
    
    # Convert the request list to a single string
    request = " ".join(args.request)
    
    logger.info(f"Loading {args.agent} agent...")
    agent = load_agent(args.agent)
    
    logger.info(f"Running {args.agent} with request: '{request}'")
    
    # Execute the agent with the provided request
    try:
        logger.info("\n=== Agent Request ===")
        logger.info(request)
        response = agent.run(request)
        logger.info("\n=== Agent Response ===")
        logger.info(response)
    except Exception as e:
        logger.error(f"Error executing agent: {str(e)}")
        traceback.logger.info_exc()
        sys.exit(1)


if __name__ == "__main__":
    # main()
    
    # # FileConverter agent test
    # agent = load_agent("FileConverter")
    # file_uri = r"C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\dummy.png"
    # response = agent.run(f"Convert this '{file_uri}' to markdown")
    # logger.info(response)
    
    # # FileOrganizer agent test
    # agent = load_agent("FileOrganizer")
    # init_dir = r'C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples'
    # output_dir = r'C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\sample_copy'
    # response = agent.run(
    #     f"Duplicate this '{init_dir}' into '{output_dir}' and its content. "
    #     "However, invert the name of file order 'hello' -> 'olleh'"
    # )
    
    # FileOrchestrator agent test
    agent = load_agent("FileOrchestrator")
    # prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    # logger.info(f"Loading prompt from file: {prompt_path}")
    # with open(prompt_path, "r") as f:
    #     prompt = f.read()
    # logger.info(f"Prompt loaded:\n{prompt}")
    # response = agent.run(prompt)
    # init_dir = r'C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\sample_copy'
    # output_dir = r'C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\sample_copy2'
    # json_filename = "image_data.json"
    # response = agent.run(
    #     f"Duplicate this '{init_dir}' into '{output_dir}' and its content. "
    #     "However, invert the name of file order 'hello.txt' -> 'olleh.txt'. Finally, "
    #     "from the duplicated files, convert all images to dictionary format and save them as JSON "
    #     f"files in the same directory as '{json_filename}'"
    # )
    logger.info(agent.visualize())