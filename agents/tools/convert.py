import os
import sys

# Add parent directory to path BEFORE other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docling.document_converter import DocumentConverter
from smolagents import Tool
from utils.logging import get_logger

# Get the logger instance
logger = get_logger(__name__)

class VideoFormatConverterTool(Tool):
    name = "video_format_converter_tool"
    description = (
        "A tool for converting video files between different formats. "
        "This tool takes an input video file and converts it to the specified output format. "
        "It can automatically determine the output format based on the extension of the output path. "
        "Supports common video formats like MP4, AVI, MKV, MOV, WebM, and FLV. "
        "Allows specifying video and audio codecs, resolution, and bitrates for fine-tuned conversions."
    )
    inputs = {
        "source_path": {
            "type": "string",
            "description": "The full path to the input video file.",
        },
        "output_path": {
            "type": "string",
            "description": "The full path where the converted video should be saved. If provided, the format will be determined from the extension.",
            "nullable": True
        },
        "output_format": {
            "type": "string",
            "description": "The desired output format (e.g., 'mp4', 'avi', 'mkv'). Only needed if output_path doesn't have an extension.",
            "nullable": True
        },
        "video_codec": {
            "type": "string",
            "description": "Video codec to use (e.g., 'h264', 'vp9', 'hevc'). If not provided, a default codec for the format will be used.",
            "nullable": True
        },
        "audio_codec": {
            "type": "string",
            "description": "Audio codec to use (e.g., 'aac', 'mp3'). If not provided, a default codec for the format will be used.",
            "nullable": True
        },
        "resolution": {
            "type": "string",
            "description": "Target resolution in format 'widthxheight' (e.g., '1920x1080', '720x480'). If not provided, the source resolution will be preserved.",
            "nullable": True
        },
        "video_bitrate": {
            "type": "string",
            "description": "Target video bitrate (e.g., '2M', '5000k'). Higher values mean better quality but larger files.",
            "nullable": True
        },
        "audio_bitrate": {
            "type": "string",
            "description": "Target audio bitrate (e.g., '192k', '320k').",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, source_path: str, output_path: str = None, output_format: str = None,
                video_codec: str = None, audio_codec: str = None, resolution: str = None,
                video_bitrate: str = None, audio_bitrate: str = None) -> str:
        """
        Converts a video file from one format to another with optional codec and quality specifications.
        
        Parameters:
            source_path (str): Path to the input video file.
            output_path (str, optional): Path where the converted video should be saved.
                If not provided, the output will be saved in the same directory with a new extension.
            output_format (str, optional): The desired output format (e.g., 'mp4', 'avi').
                Only needed if output_path doesn't specify the format through its extension.
            video_codec (str, optional): Video codec to use for the output file.
            audio_codec (str, optional): Audio codec to use for the output file.
            resolution (str, optional): Target resolution in format 'widthxheight'.
            video_bitrate (str, optional): Target video bitrate.
            audio_bitrate (str, optional): Target audio bitrate.
            
        Returns:
            str: A message indicating success or failure of the conversion.
        """
        try:
            # Import FFmpeg Python wrapper only when needed to avoid unnecessary dependencies
            import ffmpeg
            import os
            
            # Check if source file exists
            if not os.path.exists(source_path):
                return f"Error: Source video file '{source_path}' does not exist."
            
            # Determine output path and format
            if not output_path:
                if not output_format:
                    return "Error: Either output_path or output_format must be provided."
                
                # Generate output path based on source path and desired format
                base_path = os.path.splitext(source_path)[0]
                output_path = f"{base_path}.{output_format.lower()}"
            else:
                # If output_path is provided but has no extension and output_format is specified
                if not os.path.splitext(output_path)[1] and output_format:
                    output_path = f"{output_path}.{output_format.lower()}"
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Extract the output format from the extension if not explicitly provided
            if not output_format:
                output_format = os.path.splitext(output_path)[1][1:].lower()  # Remove the dot
            
            # Default codecs for common formats if not specified
            default_video_codecs = {
                'mp4': 'libx264',
                'avi': 'mpeg4',
                'mkv': 'libx264',
                'mov': 'libx264',
                'webm': 'libvpx',
                'flv': 'flv',
            }
            
            default_audio_codecs = {
                'mp4': 'aac',
                'avi': 'mp3',
                'mkv': 'aac',
                'mov': 'aac',
                'webm': 'libvorbis',
                'flv': 'aac',
            }
            
            # Use the specified codecs or the defaults for the format
            vcodec = video_codec if video_codec else default_video_codecs.get(output_format.lower())
            acodec = audio_codec if audio_codec else default_audio_codecs.get(output_format.lower())
            
            # Setup FFmpeg conversion
            stream = ffmpeg.input(source_path)
            
            # Build the output stream with specified parameters
            kwargs = {}
            
            # Add codecs if available
            if vcodec:
                kwargs['vcodec'] = vcodec
            if acodec:
                kwargs['acodec'] = acodec
                
            # Add resolution if specified
            if resolution:
                # Parse width and height from resolution string
                try:
                    width, height = map(int, resolution.lower().split('x'))
                    kwargs['s'] = f"{width}x{height}"
                except (ValueError, AttributeError):
                    return f"Error: Invalid resolution format '{resolution}'. Use format like '1920x1080'."
            
            # Add bitrates if specified
            if video_bitrate:
                kwargs['video_bitrate'] = video_bitrate
            if audio_bitrate:
                kwargs['audio_bitrate'] = audio_bitrate
            
            # Run the conversion
            output_stream = ffmpeg.output(stream, output_path, **kwargs)
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            
            return f"Video successfully converted from {source_path} to {output_path}"
            
        except ImportError:
            return "Error: FFmpeg-python is required for video conversion. Please install it with 'pip install ffmpeg-python'."
        except ffmpeg.Error as e:
            return f"Error in FFmpeg conversion: {str(e.stderr.decode('utf-8') if hasattr(e, 'stderr') else str(e))}"
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to both paths."
        except Exception as e:
            return f"Error converting video: {str(e)}"


class AudioFormatConverterTool(Tool):
    name = "audio_format_converter_tool"
    description = (
        "A tool for converting audio files between different formats. "
        "This tool takes an input audio file and converts it to the specified output format. "
        "It can automatically determine the output format based on the extension of the output path. "
        "Supports common audio formats like MP3, WAV, OGG, FLAC, AAC, and M4A. "
        "Optional codec specification allows for more control over the conversion process."
    )
    inputs = {
        "source_path": {
            "type": "string",
            "description": "The full path to the input audio file.",
        },
        "output_path": {
            "type": "string",
            "description": "The full path where the converted audio should be saved. If provided, the format will be determined from the extension.",
            "nullable": True
        },
        "output_format": {
            "type": "string",
            "description": "The desired output format (e.g., 'mp3', 'wav', 'ogg'). Only needed if output_path doesn't have an extension.",
            "nullable": True
        },
        "codec": {
            "type": "string",
            "description": "Specific audio codec to use for encoding (e.g., 'libmp3lame' for MP3, 'pcm_s16le' for WAV). If not provided, a default codec for the format will be used.",
            "nullable": True
        },
        "bitrate": {
            "type": "string", 
            "description": "The bitrate for the output file (e.g., '192k', '320k'). Higher values mean better quality but larger files.",
            "nullable": True
        },
        "sample_rate": {
            "type": "integer",
            "description": "Sample rate in Hz (e.g., 44100, 48000). If not provided, the source sample rate will be preserved.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, source_path: str, output_path: str = None, output_format: str = None, 
                codec: str = None, bitrate: str = None, sample_rate: int = None) -> str:
        """
        Converts an audio file from one format to another with optional codec specifications.
        
        Parameters:
            source_path (str): Path to the input audio file.
            output_path (str, optional): Path where the converted audio should be saved.
                If not provided, the output will be saved in the same directory with a new extension.
            output_format (str, optional): The desired output format (e.g., 'mp3', 'wav').
                Only needed if output_path doesn't specify the format through its extension.
            codec (str, optional): Specific audio codec to use for encoding.
            bitrate (str, optional): Target bitrate for the output file (e.g., '192k').
            sample_rate (int, optional): Target sample rate in Hz.
            
        Returns:
            str: A message indicating success or failure of the conversion.
        """
        try:
            # Import FFmpeg Python wrapper only when needed to avoid unnecessary dependencies
            import ffmpeg
            import os
            
            # Check if source file exists
            if not os.path.exists(source_path):
                return f"Error: Source audio file '{source_path}' does not exist."
            
            # Determine output path and format
            if not output_path:
                if not output_format:
                    return "Error: Either output_path or output_format must be provided."
                
                # Generate output path based on source path and desired format
                base_path = os.path.splitext(source_path)[0]
                output_path = f"{base_path}.{output_format.lower()}"
            else:
                # If output_path is provided but has no extension and output_format is specified
                if not os.path.splitext(output_path)[1] and output_format:
                    output_path = f"{output_path}.{output_format.lower()}"
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Extract the output format from the extension if not explicitly provided
            if not output_format:
                output_format = os.path.splitext(output_path)[1][1:].lower()  # Remove the dot
            
            # Default codecs for common formats if not specified
            default_codecs = {
                'mp3': 'libmp3lame',
                'wav': 'pcm_s16le',
                'ogg': 'libvorbis',
                'flac': 'flac',
                'aac': 'aac',
                'm4a': 'aac',
            }
            
            # Use the specified codec or the default for the format
            audio_codec = codec if codec else default_codecs.get(output_format.lower())
            
            # Setup FFmpeg conversion
            stream = ffmpeg.input(source_path)
            
            # Build the output stream with specified parameters
            kwargs = {'acodec': audio_codec} if audio_codec else {}
            
            # Add bitrate if specified
            if bitrate:
                kwargs['audio_bitrate'] = bitrate
                
            # Add sample rate if specified
            if sample_rate:
                kwargs['ar'] = sample_rate
                
            # Run the conversion
            output_stream = ffmpeg.output(stream, output_path, **kwargs)
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            
            return f"Audio successfully converted from {source_path} to {output_path}"
            
        except ImportError:
            return "Error: FFmpeg-python is required for audio conversion. Please install it with 'pip install ffmpeg-python'."
        except ffmpeg.Error as e:
            return f"Error in FFmpeg conversion: {str(e.stderr.decode('utf-8') if hasattr(e, 'stderr') else str(e))}"
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to both paths."
        except Exception as e:
            return f"Error converting audio: {str(e)}"


class ImageFormatConverterTool(Tool):
    name = "image_format_converter_tool"
    description = (
        "A tool for converting images between different formats. "
        "This tool takes an input image file and converts it to the specified output format. "
        "It can automatically determine the output format based on the extension of the output path. "
        "Supports common image formats like PNG, JPEG, GIF, BMP, TIFF, and WebP."
    )
    inputs = {
        "source_path": {
            "type": "string",
            "description": "The full path to the input image file.",
        },
        "output_path": {
            "type": "string",
            "description": "The full path where the converted image should be saved. If provided, the format will be determined from the extension.",
            "nullable": True
        },
        "output_format": {
            "type": "string",
            "description": "The desired output format (e.g., 'png', 'jpg', 'gif'). Only needed if output_path doesn't have an extension.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, source_path: str, output_path: str = None, output_format: str = None) -> str:
        """
        Converts an image from one format to another.
        
        Parameters:
            source_path (str): Path to the input image file.
            output_path (str, optional): Path where the converted image should be saved.
                If not provided, the output will be saved in the same directory with a new extension.
            output_format (str, optional): The desired output format (e.g., 'png', 'jpg').
                Only needed if output_path doesn't specify the format through its extension.
            
        Returns:
            str: A message indicating success or failure of the conversion.
        """
        try:
            # Import PIL only when needed to avoid unnecessary dependencies
            from PIL import Image
            import os
            
            # Check if source file exists
            if not os.path.exists(source_path):
                return f"Error: Source image '{source_path}' does not exist."
            
            # Determine output path and format
            if not output_path:
                if not output_format:
                    return "Error: Either output_path or output_format must be provided."
                
                # Generate output path based on source path and desired format
                base_path = os.path.splitext(source_path)[0]
                output_path = f"{base_path}.{output_format.lower()}"
            else:
                # If output_path is provided but has no extension and output_format is specified
                if not os.path.splitext(output_path)[1] and output_format:
                    output_path = f"{output_path}.{output_format.lower()}"
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Extract the output format from the extension if not explicitly provided
            if not output_format:
                output_format = os.path.splitext(output_path)[1][1:]  # Remove the dot
            
            # Open the image and convert it
            with Image.open(source_path) as img:
                # Check if the format is different before saving
                source_format = os.path.splitext(source_path)[1][1:].lower()
                target_format = output_format.lower()
                
                # Handle JPEG format naming convention
                if target_format in ('jpg', 'jpeg'):
                    save_format = 'JPEG'
                else:
                    save_format = target_format.upper()
                
                # For formats that support transparency
                if save_format in ('PNG', 'GIF', 'WEBP'):
                    # Convert to RGBA if the image has transparency
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        img = img.convert('RGBA')
                    else:
                        img = img.convert('RGB')
                else:
                    # Convert to RGB for formats that don't support transparency
                    img = img.convert('RGB')
                
                # Save the image in the specified format
                img.save(output_path, format=save_format)
                
            return f"Image successfully converted from {source_path} to {output_path}"
            
        except ImportError:
            return "Error: Pillow (PIL) library is required for image conversion. Please install it with 'pip install Pillow'."
        except PermissionError:
            return f"Error: Permission denied. Check if you have access rights to both paths."
        except Exception as e:
            return f"Error converting image: {str(e)}"


class File2DocumentTool(Tool):
    name = "file_to_document_tool"
    description = (
        "A tool for converting files from various formats (PDF, DOCX, XLSX, HTML, images, and more.) into "
        "a unified document structured representation. The output can be formatted as Markdown, HTML, plain text, dictionary, "
        "or a list of document tokens."
        "\n\n"
        "The source input can be a URL or a local file path."
    )
    inputs = {
        "source": {
            "type": "string",
            "description": "A URL or local file path to the document to be converted.",
        },
        "output_format": {
            "type": "string",
            "description": "The desired output format. Supported values are: 'markdown', 'dict', 'text', 'document_tokens', 'html'.",
            "nullable": True  # Add this line to mark as nullable
        }
    }
    output_type = "string"


    def forward(self, source: str, output_format: str = "markdown") -> str:
        """
        Converts a source document to a specified output format.

        Parameters:
            source (str): The input document as a string.
            output_format (str): The desired output format. Supported formats are
                                "markdown", "html", "dict", "text", and "document_tokens".

        Returns:
            str: The converted document in the desired format, or an error message if the conversion fails.
        """
        converter = DocumentConverter()
        available_formats = {"markdown", "html", "dict", "text", "document_tokens"}

        fmt = output_format.lower()
        if fmt not in available_formats:
            return (
                f"Unsupported output format: {output_format}. "
                f"Supported formats are: {', '.join(sorted(available_formats))}."
            )

        try:
            # Convert the document using Docling's DocumentConverter
            result = converter.convert(source)

            # Map output formats to their corresponding export functions
            export_methods = {
                "markdown": result.document.export_to_markdown,
                "html": result.document.export_to_html,
                "dict": result.document.export_to_dict,
                "text": result.document.export_to_text,
                "document_tokens": lambda: result.export_to_document_tokens,
            }
            # Execute and return the conversion result
            return export_methods[fmt]()
        except Exception as e:
            return f"Error converting document: {str(e)}"
