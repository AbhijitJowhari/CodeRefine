# CodeRefine

CodeRefine is a framework designed to improve the quality of code implementations generated for research papers by Large Language Models (LLMs), with a specific focus on GPT-4. This repository contains the pipeline for the CodeRefine system, aiming to enhance code synthesis from research papers through a structured and iterative process.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Overview](#pipeline-overview)
- [Directory Structure](#directory-structure)
- [API Keys](#api-keys)
- [Running the Pipeline](#running-the-pipeline)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the cloned directory:
   ```bash
   cd CodeRefine
   ```

## Usage

### Pipeline Overview

The CodeRefine pipeline consists of several steps designed to extract relevant information from research papers, construct knowledge graphs, and iteratively refine the code output by querying related research papers and utilizing LLMs.

### Directory Structure

Create the following directories in the root of the repository:

```bash
mkdir query_paper query_paper_xml ref_papers ref_papers_xml
```

- `query_paper`: Add the input paper to this directory.
- `query_paper_xml`: This directory will store the XML representation of the input paper.
- `ref_papers`: Add both the input paper and its references to this directory.
- `ref_papers_xml`: This directory will store the XML representation of the reference papers.

### API Keys

You need to generate API keys for the following services:
>1. [MixedBreadAI](https://www.mixedbread.ai/api-reference/authentication)
>2. [OpenAI](https://platform.openai.com/api-keys)
>3. [Groq](https://console.groq.com/keys)

Set these API keys as environment variables in your terminal:

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
export GROQ_API_KEY="<your_groq_api_key>"
export MXBAI_API_KEY="<your_mixedbread_api_key_here>"
```

## Running the Pipeline

Execute the following command from the root directory of the repository:

```bash
python3 main.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.