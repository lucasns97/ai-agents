# ai-agents

## Overview

This repository serves as my personal sandbox for experimenting with AI agent architectures and implementations. Here I explore various approaches to building autonomous intelligent systems that can perceive, reason, and act in different environments.

## Project Goals

- Explore different AI agent architectures (reactive, deliberative, hybrid)
- Implement agents using various frameworks and technologies
- Experiment with multi-agent systems and communication
- Test learning-based agents using reinforcement learning
- Build specialized agents for file manipulation and document processing
- Document findings and best practices for future reference

## Getting Started

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-agents.git
cd ai-agents

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Agents

You can run any of the implemented agents using the runner script:

```bash
python agents/run.py [agent_name] [request]
```

For example:

```bash
python agents/run.py FileOrchestrator "Generate an image of a cat wearing a hat and save it as 'cat.jpg'"
```

### Project Structure

```
ai-agents/
├── agents/                   # Agent implementations
│   ├── FileConverter.py      # File format conversion agent
│   ├── FileOrchestrator.py   # Orchestration of multiple agents
│   ├── FileOrganizer.py      # File system operations agent
│   ├── ImageCreator.py       # Image generation agent
│   ├── PdfEditor.py          # PDF manipulation agent
│   └── tools/                # Tools used by agents
│       ├── convert.py        # File conversion tools
│       ├── edit_pdf.py       # PDF manipulation tools
│       └── system.py         # File system operation tools
├── environments/       # Test environments
├── utils/              # Helper functions
├── experiments/        # Experiment scripts
├── config/             # Configuration files
├── samples/            # Sample files for testing
├── .sandbox/           # Sandbox area for agent operations
└── docs/               # Documentation
```

### Implemented Agents

#### FileOrchestrator

Coordinates multiple specialized agents to perform complex file tasks. This is the main agent that can delegate work to other agents.

<details>
<summary>Agent Definition</summary>
CodeAgent | gpt-4o
├── ✅ Authorized imports: ['os', 'shutil']
├── 🛠️ Tools:
│   ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│   ┃ Name         ┃ Description                                   ┃ Arguments                                       ┃
│   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   │ final_answer │ Provides a final answer to the given problem. │ answer (`any`): The final answer to the problem │
│   └──────────────┴───────────────────────────────────────────────┴─────────────────────────────────────────────────┘
└── 🤖 Managed agents:
    ├── FileConverter | ToolCallingAgent | gpt-4o-mini
    │   ├── 📝 Description: Converts files from one format to another.
    │   └── 🛠️ Tools:
    │       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │       ┃ Name                        ┃ Description                                   ┃ Arguments                                     ┃
    │       ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │       │ file_to_document_tool       │ A tool for converting files from various      │ source (`string`): A URL or local file path   │
    │       │                             │ formats (PDF, DOCX, XLSX, HTML, images, and   │ to the document to be converted.              │
    │       │                             │ more.) into a unified document structured     │ output_format (`string`): The desired output  │
    │       │                             │ representation. The output can be formatted   │ format. Supported values are: 'markdown',     │
    │       │                             │ as Markdown, HTML, plain text, dictionary, or │ 'dict', 'text', 'document_tokens', 'html'.    │
    │       │                             │ a list of document tokens.                    │                                               │
    │       │                             │                                               │                                               │
    │       │                             │ The source input can be a URL or a local file │                                               │
    │       │                             │ path.                                         │                                               │
    │       │ image_format_converter_tool │ A tool for converting images between          │ source_path (`string`): The full path to the  │
    │       │                             │ different formats. This tool takes an input   │ input image file.                             │
    │       │                             │ image file and converts it to the specified   │ output_path (`string`): The full path where   │
    │       │                             │ output format. It can automatically determine │ the converted image should be saved. If       │
    │       │                             │ the output format based on the extension of   │ provided, the format will be determined from  │
    │       │                             │ the output path. Supports common image        │ the extension.                                │
    │       │                             │ formats like PNG, JPEG, GIF, BMP, TIFF, and   │ output_format (`string`): The desired output  │
    │       │                             │ WebP.                                         │ format (e.g., 'png', 'jpg', 'gif'). Only      │
    │       │                             │                                               │ needed if output_path doesn't have an         │
    │       │                             │                                               │ extension.                                    │
    │       │ audio_format_converter_tool │ A tool for converting audio files between     │ source_path (`string`): The full path to the  │
    │       │                             │ different formats. This tool takes an input   │ input audio file.                             │
    │       │                             │ audio file and converts it to the specified   │ output_path (`string`): The full path where   │
    │       │                             │ output format. It can automatically determine │ the converted audio should be saved. If       │
    │       │                             │ the output format based on the extension of   │ provided, the format will be determined from  │
    │       │                             │ the output path. Supports common audio        │ the extension.                                │
    │       │                             │ formats like MP3, WAV, OGG, FLAC, AAC, and    │ output_format (`string`): The desired output  │
    │       │                             │ M4A. Optional codec specification allows for  │ format (e.g., 'mp3', 'wav', 'ogg'). Only      │
    │       │                             │ more control over the conversion process.     │ needed if output_path doesn't have an         │
    │       │                             │                                               │ extension.                                    │
    │       │                             │                                               │ codec (`string`): Specific audio codec to use │
    │       │                             │                                               │ for encoding (e.g., 'libmp3lame' for MP3,     │
    │       │                             │                                               │ 'pcm_s16le' for WAV). If not provided, a      │
    │       │                             │                                               │ default codec for the format will be used.    │
    │       │                             │                                               │ bitrate (`string`): The bitrate for the       │
    │       │                             │                                               │ output file (e.g., '192k', '320k'). Higher    │
    │       │                             │                                               │ values mean better quality but larger files.  │
    │       │                             │                                               │ sample_rate (`integer`): Sample rate in Hz    │
    │       │                             │                                               │ (e.g., 44100, 48000). If not provided, the    │
    │       │                             │                                               │ source sample rate will be preserved.         │
    │       │ video_format_converter_tool │ A tool for converting video files between     │ source_path (`string`): The full path to the  │
    │       │                             │ different formats. This tool takes an input   │ input video file.                             │
    │       │                             │ video file and converts it to the specified   │ output_path (`string`): The full path where   │
    │       │                             │ output format. It can automatically determine │ the converted video should be saved. If       │
    │       │                             │ the output format based on the extension of   │ provided, the format will be determined from  │
    │       │                             │ the output path. Supports common video        │ the extension.                                │
    │       │                             │ formats like MP4, AVI, MKV, MOV, WebM, and    │ output_format (`string`): The desired output  │
    │       │                             │ FLV. Allows specifying video and audio        │ format (e.g., 'mp4', 'avi', 'mkv'). Only      │
    │       │                             │ codecs, resolution, and bitrates for          │ needed if output_path doesn't have an         │
    │       │                             │ fine-tuned conversions.                       │ extension.                                    │
    │       │                             │                                               │ video_codec (`string`): Video codec to use    │
    │       │                             │                                               │ (e.g., 'h264', 'vp9', 'hevc'). If not         │
    │       │                             │                                               │ provided, a default codec for the format will │
    │       │                             │                                               │ be used.                                      │
    │       │                             │                                               │ audio_codec (`string`): Audio codec to use    │
    │       │                             │                                               │ (e.g., 'aac', 'mp3'). If not provided, a      │
    │       │                             │                                               │ default codec for the format will be used.    │
    │       │                             │                                               │ resolution (`string`): Target resolution in   │
    │       │                             │                                               │ format 'widthxheight' (e.g., '1920x1080',     │
    │       │                             │                                               │ '720x480'). If not provided, the source       │
    │       │                             │                                               │ resolution will be preserved.                 │
    │       │                             │                                               │ video_bitrate (`string`): Target video        │
    │       │                             │                                               │ bitrate (e.g., '2M', '5000k'). Higher values  │
    │       │                             │                                               │ mean better quality but larger files.         │
    │       │                             │                                               │ audio_bitrate (`string`): Target audio        │
    │       │                             │                                               │ bitrate (e.g., '192k', '320k').               │
    │       │ final_answer                │ Provides a final answer to the given problem. │ answer (`any`): The final answer to the       │
    │       │                             │                                               │ problem                                       │
    │       └─────────────────────────────┴───────────────────────────────────────────────┴───────────────────────────────────────────────┘
    ├── FileOrganizer | CodeAgent | gpt-4o-mini
    │   ├── ✅ Authorized imports: ['os', 'shutil']
    │   ├── 📝 Description: Organizes and manages files in the local file system.
    │   └── 🛠️ Tools:
    │       ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │       ┃ Name             ┃ Description                                         ┃ Arguments                                          ┃
    │       ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │       │ rename_file_tool │ A tool for renaming or moving files in the file     │ source_path (`string`): The full path to the file  │
    │       │                  │ system. This tool can move a file from one location │ you want to rename or move.                        │
    │       │                  │ to another, or simply rename it within the same     │ target_path (`string`): The full path to the new   │
    │       │                  │ directory. The tool will check if the source file   │ location and/or filename.                          │
    │       │                  │ exists and if the destination doesn't already exist │ force_overwrite (`boolean`): If True, will         │
    │       │                  │ to prevent accidental overwrites.                   │ overwrite the destination file if it exists.       │
    │       │                  │                                                     │ Default is False.                                  │
    │       │ delete_file_tool │ A tool for deleting files from the file system.     │ file_path (`string`): The full path to the file    │
    │       │                  │ This tool can permanently remove a file from the    │ that needs to be deleted.                          │
    │       │                  │ specified path. By default, the tool requires       │ confirm (`boolean`): Confirmation flag that must   │
    │       │                  │ confirmation to prevent accidental deletions.       │ be explicitly set to True to delete the file. This │
    │       │                  │                                                     │ helps prevent accidental deletions.                │
    │       │ copy_file_tool   │ A tool for copying files from one location to       │ source_path (`string`): The full path to the file  │
    │       │                  │ another in the file system. This tool can duplicate │ you want to copy.                                  │
    │       │                  │ a file while leaving the original intact. The tool  │ destination_path (`string`): The full path where   │
    │       │                  │ will check if the source file exists and if the     │ the file should be copied to, including the        │
    │       │                  │ destination already exists to prevent accidental    │ filename.                                          │
    │       │                  │ overwrites.                                         │ force_overwrite (`boolean`): If True, will         │
    │       │                  │                                                     │ overwrite the destination file if it exists.       │
    │       │                  │                                                     │ Default is False.                                  │
    │       │ final_answer     │ Provides a final answer to the given problem.       │ answer (`any`): The final answer to the problem    │
    │       └──────────────────┴─────────────────────────────────────────────────────┴────────────────────────────────────────────────────┘
    ├── PdfEditor | ToolCallingAgent | gpt-4o-mini
    │   ├── 📝 Description: Edits PDF files such as merging, splitting, rotating, watermarking, and adding password protection.
    │   └── 🛠️ Tools:
    │       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │       ┃ Name                     ┃ Description                                     ┃ Arguments                                      ┃
    │       ┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │       │ merge_pdf_tool           │ A tool for merging multiple PDF files into one  │ input_files (`array`): An array of file paths  │
    │       │                          │ document. Provide an array of file paths for    │ to the PDF files to be merged.                 │
    │       │                          │ the PDFs to be merged and specify the output    │ output_file (`string`): The file path for the  │
    │       │                          │ file path for the merged PDF.                   │ resulting merged PDF.                          │
    │       │ split_pdf_tool           │ A tool for splitting a PDF file into individual │ file_path (`string`): The file path of the PDF │
    │       │                          │ page PDFs. Provide the file path of the PDF to  │ to be split.                                   │
    │       │                          │ split and an output directory where the         │ output_dir (`string`): The directory where the │
    │       │                          │ resulting PDF pages will be saved.              │ split PDF files will be saved.                 │
    │       │ rotate_pdf_tool          │ A tool for rotating specified pages in a PDF    │ file_path (`string`): The file path of the PDF │
    │       │                          │ file by a given angle. Provide the PDF file     │ to be rotated.                                 │
    │       │                          │ path, a list of page numbers (1-indexed) to     │ output_file (`string`): The file path for the  │
    │       │                          │ rotate, the rotation angle in degrees (must be  │ rotated PDF output.                            │
    │       │                          │ a multiple of 90), and the output file path.    │ page_numbers (`array`): An array of page       │
    │       │                          │                                                 │ numbers (1-indexed) to rotate. All other pages │
    │       │                          │                                                 │ remain unchanged.                              │
    │       │                          │                                                 │ angle (`integer`): The angle in degrees to     │
    │       │                          │                                                 │ rotate the specified pages (must be a multiple │
    │       │                          │                                                 │ of 90).                                        │
    │       │ watermark_pdf_tool       │ A tool for adding an image watermark to each    │ file_path (`string`): The file path of the PDF │
    │       │                          │ page of a PDF file. Provide the PDF file path,  │ to which the watermark will be added.          │
    │       │                          │ the image file to be used as the watermark, and │ watermark_image (`string`): The file path of   │
    │       │                          │ the placement parameters (x, y, width, and      │ the image to be used as a watermark.           │
    │       │                          │ height in points). The watermark image will be  │ output_file (`string`): The file path for the  │
    │       │                          │ placed over each PDF page at the specified      │ watermarked PDF output.                        │
    │       │                          │ location.                                       │ x (`number`): The x-coordinate (in points) for │
    │       │                          │                                                 │ the placement of the watermark on each PDF     │
    │       │                          │                                                 │ page.                                          │
    │       │                          │                                                 │ y (`number`): The y-coordinate (in points) for │
    │       │                          │                                                 │ the placement of the watermark on each PDF     │
    │       │                          │                                                 │ page.                                          │
    │       │                          │                                                 │ width (`number`): The width (in points) of the │
    │       │                          │                                                 │ watermark image.                               │
    │       │                          │                                                 │ height (`number`): The height (in points) of   │
    │       │                          │                                                 │ the watermark image.                           │
    │       │ add_password_to_pdf_tool │ A tool for adding password protection to a PDF  │ file_path (`string`): The file path of the PDF │
    │       │                          │ file. Provide the file path of the PDF to       │ to be password-protected.                      │
    │       │                          │ secure, the password to set, and the output     │ password (`string`): The password to apply to  │
    │       │                          │ file path for the encrypted PDF. The resulting  │ the PDF. Users will need this password to open │
    │       │                          │ PDF will require the provided password to be    │ the file.                                      │
    │       │                          │ opened.                                         │ output_file (`string`): The file path for the  │
    │       │                          │                                                 │ output, password-protected PDF.                │
    │       │ final_answer             │ Provides a final answer to the given problem.   │ answer (`any`): The final answer to the        │
    │       │                          │                                                 │ problem                                        │
    │       └──────────────────────────┴─────────────────────────────────────────────────┴────────────────────────────────────────────────┘
    └── ImageCreator | ToolCallingAgent | gpt-4o-mini
        ├── 📝 Description: Creates and saves AI-generated images based on text descriptions.
        └── 🛠️ Tools:
            ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ Name            ┃ Description                                         ┃ Arguments                                           ┃
            ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
            │ image_generator │ This tool creates an image according to a prompt,   │ prompt (`string`): The image generator prompt.      │
            │                 │ which is a text description.                        │ Don't hesitate to add details in the prompt to make │
            │                 │                                                     │ the image look better, like 'high-res,              │
            │                 │                                                     │ photorealistic', etc.                               │
            │ save_image_tool │ A tool for saving a PIL image to the specified      │ image (`object`): A PIL Image object to be saved.   │
            │                 │ path. Provide the PIL image object and the desired  │ filename (`string`): The desired filename including │
            │                 │ filename including extension. If no filename is     │ extension (e.g., 'my_image.png').                   │
            │                 │ provided, a unique filename will be generated.      │ output_dir (`string`): Directory where the image    │
            │                 │                                                     │ should be saved. Defaults to current working        │
            │                 │                                                     │ directory.                                          │
            │ final_answer    │ Provides a final answer to the given problem.       │ answer (`any`): The final answer to the problem     │
            └─────────────────┴─────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
</details>

#### FileConverter

Converts files between different formats:

- Convert images between formats (PNG, JPEG, GIF, BMP, TIFF, WebP)
- Convert audio files (MP3, WAV, OGG, FLAC, AAC, M4A)
- Convert video files (MP4, AVI, MKV, MOV, WebM, FLV)
- Convert documents to structured formats (Markdown, HTML, plain text)

#### FileOrganizer

Performs file system operations:

- Copy files
- Delete files
- Rename or move files

#### PdfEditor
Advanced PDF manipulation operations:

- Split PDFs into individual pages
- Merge multiple PDFs into one document
- Add watermarks to PDFs
- Rotate PDF pages
- Add password protection to PDFs

#### ImageCreator
Generates images using AI:

- Creates images from text descriptions
- Saves generated images to specified paths

### Technologies
- Python
- Machine learning frameworks (TensorFlow/PyTorch)
- Large Language Models (LLMs)
- Langchain and other agent frameworks
- OpenAI Gym/Gymnasium for environments
- smolagents framework for agent implementation
- OpenAI models (GPT-4o, GPT-4o-mini) for reasoning
- Hugging Face models for specialized tasks
- PyPDF2 for PDF manipulation
- PIL for image processing
- ffmpeg for audio/video conversion
- docling for document conversion

## Technologies

- Python
- Machine learning frameworks (TensorFlow/PyTorch)
- Large Language Models (LLMs)
- Langchain and other agent frameworks
- OpenAI Gym/Gymnasium for environments

## Key Research Areas

- **Autonomous Decision Making**: Building agents that make intelligent decisions
- **Agent Communication**: Protocols for agent-to-agent communication
- **Learning from Experience**: Implementing reinforcement learning algorithms
- **Tool Usage**: Agents that effectively use external tools and APIs
- **Emergent Behaviors**: Studying complex behaviors in multi-agent systems

## License

This project is under the MIT License - see the LICENSE file for details.

## Future Work

- [ ] Implement a basic reactive agent
- [ ] Create a simple environment for agent testing
- [ ] Add reinforcement learning capabilities
- [ ] Explore LLM-based agent architectures
- [ ] Build a multi-agent simulation