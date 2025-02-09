# X-Copilot (RAG-based Application)

## Overview
X-Copilot is an advanced Retrieval-Augmented Generation (RAG) application powered by DeepSeek 1.5B and web scraping capabilities using BeautifulSoup. It efficiently processes and retrieves relevant information from multiple sources, enhancing AI-driven knowledge extraction and contextual responses.


## Features
- **Large Language Model (LLM) Integration**: Utilizes DeepSeek 1.5B for generating intelligent responses.
- **Web Scraping**: Employs BeautifulSoup to extract relevant data from web sources.
- **Flask API**: Serves as a backend API for seamless integration.
- **Efficient Data Retrieval**: Implements RAG to fetch and process contextual information dynamically.
# Installation Guide

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- pip (Python package manager)
- Ollama (for running the DeepSeek model)

## Installation Steps

### 1. Clone the Repository

```shell
# Clone the repository and navigate to project directory
git clone https://github.com/shiv10000/X-Copilot
cd x-copilot
```

### 2. Install Dependencies

```shell
# Install required Python packages
pip install -r requirements.txt
```

### 3. Set Up DeepSeek Model

```shell
# Run DeepSeek model using Ollama
ollama run deepseek-r1:1.5b
```

### 4. Launch Application

```shell
# Start the Flask application
python app_gui.py
```

## Troubleshooting

If you encounter any issues during installation:

```shell
# Check Python version
python --version

# Verify pip installation
pip --version

# Check Ollama status
ollama ps
```

