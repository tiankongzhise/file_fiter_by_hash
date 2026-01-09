# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A file filtering tool that classifies and deduplicates files/folders using SHA256, SHA1, and MD5 hashes. Items are classified into categories (big files, zip files, normal files, empty folders, etc.) and moved to target directories (backup, processing, deletion, etc.) based on hash comparisons against a database.

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

### Core Flow (6-Step Filter Pipeline in `service/fiter_file.py`)

1. **step_one**: Classify top-level items as files or folders
2. **step_two**: Further classify folders as normal, big (>100 files), or empty
3. **step_three**: Process big folders - check by name/size against special folder database
4. **step_four**: Delete empty folders
5. **step_five**: Process normal folders - calculate hash and check against database
6. **step_six**: Process files - calculate hash and check against database

### Key Modules

| Path | Purpose |
|------|---------|
| `service/calculate_hash_service/` | Hash computation (SHA256/MD5/SHA1) using 500MB chunks |
| `service/classfiy_service.py` | Item classification (big_file, zip_file, normal_file, etc.) |
| `control/filter_process.py` | Orchestrates classification workflow |
| `core/sqlite_core/` | Singleton-based database infrastructure (engine, model, schema managers) |
| `config/classify_config.py` | Source/target paths, size thresholds (500MB default), max folder file count (100) |
| `logger/` | Dual-output logging (console + SQLite database) |

### Data Flow

`pre_classify()` in `control/filter_process.py` is the main entry point that:
1. Retrieves all file paths using cached `get_all_file_path()`
2. Runs items through `FilterFile` 6-step pipeline
3. Uses `classify_item()`/`classify_folder()` for categorization
4. Compares hashes via `calculate_file_hash()` against database
5. Moves files via `file_operation.py` utilities

### Key Patterns

- **Singletons**: `SQLiteEngineManager`, `SQLiteModelManager`, `SQLiteSchemaManager` for database management
- **Pydantic Models**: `HashInfo`, `HashResult`, `LoggerInfo` for data validation
- **Service Codes**: Operations return tracked codes (e.g., `'F010010011'` for "文件移动成功")
- **Pathlib**: All file operations use `pathlib.Path` (Windows-compatible)
