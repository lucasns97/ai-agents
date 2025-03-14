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