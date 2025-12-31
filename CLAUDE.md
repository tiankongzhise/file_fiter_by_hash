# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A file filtering tool that uses SHA256 and MD5 hashes to identify duplicate or already-stored files. Uses multiprocessing for efficient batch processing.

## Commands

```bash
# Run the main program
uv run python main.py

# Add dependencies
uv add <package>

# Sync dependencies
uv sync
```

## Architecture

- **main.py**: Main entry point containing:
  - `calculate_hash()` / `calculate_file_hash()`: Single file hash computation (SHA256/MD5)
  - `calculate_folder_hash()`: Folder hash by combining all file hashes
  - `process_file()`: Multiprocessing worker for file processing
  - `process_folder()`: Folder-level hash processing
  - `record_results()`: Async JSON result writer
  - `main()`: Orchestrates multiprocessing pool (max 8 workers)
