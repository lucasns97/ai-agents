import os
import sys

# Add parent directory to path BEFORE other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import shutil
from utils.logging import get_logger
from smolagents import Tool

# Get the logger instance
logger = get_logger(__name__)

class DeleteFileTool(Tool):
    name = "delete_file_tool"
    description = (
        "A tool for deleting files from the file system. "
        "This tool can permanently remove a file from the specified path. "
        "By default, the tool requires confirmation to prevent accidental deletions."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "The full path to the file that needs to be deleted.",
        },
        "confirm": {
            "type": "boolean",
            "description": "Confirmation flag that must be explicitly set to True to delete the file. This helps prevent accidental deletions.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, file_path: str, confirm: bool = False) -> str:
        """
        Deletes a file at the specified path.
        
        Parameters:
            file_path (str): Path to the file to be deleted.
            confirm (bool): Explicit confirmation that the file should be deleted.
            
        Returns:
            str: A message indicating success or failure of the deletion.
        """
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."
            
            # Check if it's actually a file (not a directory)
            if not os.path.isfile(file_path):
                return f"Error: '{file_path}' is not a file. Use a different tool to delete directories."
            
            # Check for confirmation
            if not confirm:
                return (
                    f"Deletion requires confirmation. "
                    f"To delete '{file_path}', please call this tool again with confirm=True."
                )
            
            # Delete the file
            os.remove(file_path)
            
            return f"File '{file_path}' successfully deleted."
            
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to delete this file."
        except OSError as e:
            return f"Error deleting file: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


class CopyFileTool(Tool):
    name = "copy_file_tool"
    description = (
        "A tool for copying files from one location to another in the file system. "
        "This tool can duplicate a file while leaving the original intact. "
        "The tool will check if the source file exists and if the destination already exists "
        "to prevent accidental overwrites."
    )
    inputs = {
        "source_path": {
            "type": "string",
            "description": "The full path to the file you want to copy.",
        },
        "destination_path": {
            "type": "string",
            "description": "The full path where the file should be copied to, including the filename.",
        },
        "force_overwrite": {
            "type": "boolean",
            "description": "If True, will overwrite the destination file if it exists. Default is False.",
            "nullable": True
        }
    }
    output_type = "string"


    def forward(self, source_path: str, destination_path: str, force_overwrite: bool = False) -> str:
        """
        Copies a file from source_path to destination_path.

        Parameters:
            source_path (str): Path to the file that needs to be copied.
            destination_path (str): Path where the file should be copied to.
            force_overwrite (bool): Whether to overwrite existing files at the destination.

        Returns:
            str: A message indicating success or failure of the copy operation.
        """
        try:
            # Check if source file exists
            if not os.path.exists(source_path):
                return f"Error: Source file '{source_path}' does not exist."
            
            # Check if source is a file (not a directory)
            if not os.path.isfile(source_path):
                return f"Error: '{source_path}' is not a file. Use a different tool to copy directories."
            
            # Check if target file already exists and force_overwrite is False
            if os.path.exists(destination_path) and not force_overwrite:
                return f"Error: Destination path '{destination_path}' already exists. Use force_overwrite=True to override."
            
            # Create destination directory if it doesn't exist
            destination_dir = os.path.dirname(destination_path)
            if destination_dir and not os.path.exists(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)
            
            # Perform the copy operation
            shutil.copy2(source_path, destination_path)
            
            return f"File successfully copied from '{source_path}' to '{destination_path}'."
            
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to both paths."
        except Exception as e:
            return f"Error copying file: {str(e)}"


class RenameFileTool(Tool):
    name = "rename_file_tool"
    description = (
        "A tool for renaming or moving files in the file system. "
        "This tool can move a file from one location to another, or simply rename it within the same directory. "
        "The tool will check if the source file exists and if the destination doesn't already exist to prevent accidental overwrites."
    )
    inputs = {
        "source_path": {
            "type": "string",
            "description": "The full path to the file you want to rename or move.",
        },
        "target_path": {
            "type": "string",
            "description": "The full path to the new location and/or filename.",
        },
        "force_overwrite": {
            "type": "boolean",
            "description": "If True, will overwrite the destination file if it exists. Default is False.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, source_path: str, target_path: str, force_overwrite: bool = False) -> str:
        """
        Renames or moves a file from source_path to target_path.
        
        Parameters:
            source_path (str): Path to the existing file.
            target_path (str): Path to the new location/filename.
            force_overwrite (bool): Whether to overwrite existing files at the destination.
            
        Returns:
            str: A message indicating success or failure.
        """
        try:
            # Check if source file exists
            if not os.path.exists(source_path):
                return f"Error: Source file '{source_path}' does not exist."
            
            # Check if source is a file (not a directory)
            if not os.path.isfile(source_path):
                return f"Error: '{source_path}' is not a file."
            
            # Check if target file already exists and force_overwrite is False
            if os.path.exists(target_path) and not force_overwrite:
                return f"Error: Target path '{target_path}' already exists. Use force_overwrite=True to override."
            
            # Create target directory if it doesn't exist
            target_dir = os.path.dirname(target_path)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            
            # Perform the move/rename operation
            shutil.move(source_path, target_path)
            
            return f"File successfully moved/renamed from '{source_path}' to '{target_path}'."
            
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to both paths."
        except Exception as e:
            return f"Error renaming/moving file: {str(e)}"
