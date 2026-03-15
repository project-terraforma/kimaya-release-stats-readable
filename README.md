# Release Stats Made Readable

**Exploring Overture Maps release statistics through natural language using Large Language Models**

Winter 2026 — Project B  
Contributor: **Kimaya Basu**

---

## Overview

Traditional dashboards display fixed charts and tables that limit how users explore complex datasets. When analyzing large geospatial releases from Overture Maps, users often want to ask detailed questions that dashboards were never designed to answer.

This project introduces a different approach: transforming Overture’s monthly release statistics into a **single LLM-readable context file**.

The generated file consolidates:

- Key statistical metrics from release data
- Schema and theme descriptions
- Structured summaries of dataset changes
- Context prompts optimized for LLM interpretation

Instead of navigating dashboards, users can paste the generated file into an LLM such as **ChatGPT, Claude, or Gemini** and immediately begin exploring the dataset using **natural language queries**.

---

## Features

### LLM-Readable Data Context
- Converts Overture release statistics into **structured natural language summaries**
- Consolidates metrics from multiple datasets into a **single context file**
- Includes schema explanations and dataset descriptions

### Local Web Interface
A simple local interface allows users to preview and download the generated summary file.

Features include:

- Scrollable preview for large summaries
- One-click file download
- Copy-to-clipboard functionality
- Clean interface for browsing generated summaries
- Runs locally using Python

### Data Processing Pipeline
The backend pipeline:

1. Parses Overture release metrics
2. Cleans and standardizes statistical outputs
3. Consolidates multiple summaries into one file
4. Produces an LLM-optimized text file

This ensures the generated file contains the context required for accurate LLM reasoning.

---

## Project Structure

```
kimaya-release-stats-readable/

├── README.md
├── LICENSE
│
├── config.py
├── main.py
├── main2.py
│
├── parseFile.py
├── metrics_cleaner.py
│
├── consolidate_outs.py
├── contextGen.py
│
├── openrouter_client.py
├── getResponses.py
├── getEvals.py
│
├── out2.txt
├── test_sample_questions.csv
│
└── site_docs/
    └── app.py
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/kimaya-release-stats-readable.git
cd kimaya-release-stats-readable
```


### 2. Generate the LLM Context File

```bash
python main.py
```
or:

```bash
python main2.py
```

This will:

- Parse Overture release statistics
- Generate structured summaries
- Consolidate outputs into a single file
- * Key difference between main and main2 is that main.py takes in all data at once, generating one context file while main2.py summarizes data based on theme categorizations first, then compiles multiple outputted summary files into one final text file

Example output:

```
out.txt
```

---

## Run the Web Interface Locally

Navigate to the web interface folder:

```bash
cd site_docs
python -m http.server 8000
```

Then open:

```
http://localhost:8000
```

The interface allows you to:

- View the generated summary
- Copy the full context
- Download the summary file
- Paste it into your preferred LLM

---

## Example Queries

After loading the context file into an LLM, users can ask questions.

Sample questions askedduing testing can be found in test_sample_questions.csv

---

## 🛣️ Future Improvements

- Automated monthly release ingestion
- Integrated LLM query interface
- Visualization generation from prompts
- Multi-release comparison summaries
- Expanded dataset coverage

*Last Updated: March 2026*
