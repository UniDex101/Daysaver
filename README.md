# Daysaver

A simple, lightweight command-line tool to save and manage important dates.

## Features

- Add, remove, list, and search saved dates
- Persistent storage across sessions (platform-specific data directory)
- Today's date quick-add with `t`
- Flexible search with filters (year, month, day) or legacy string search
- Clean, colorful interface with ASCII logo
- Cross-platform (Windows, macOS, Linux)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Unidex101/daysaver.git
   cd daysaver
   ```
2. Make the script executable (Linux/macOS):
   ```bash
   chmod +x Daysaver.py
   ```
3. Run it
   ```bash
   ./Daysaver.py
   ```
   OR:
   ```
   python3 Daysaver.py
   ```

**Dependencies**: Only standard Python libraries + ezclear for screen clearing.

Install `ezclear` if needed:

```bash
pip install ezclear
```

## Usage
Launch the program and use these commands:
- `l` - List all saved dates
- `a YYYY.MM.DD` - Add a new date (e.g., `a 2026.06.25`)
- `r YYYY.MM.DD` - Remove a date
- `s [filters]` - Search dates (see help for examples)
- `t` - Add today's date
- `h` - Show help menu
- `c` - Clear screen
- `q` - Quit

## Storage Location

- Windows: `~/AppData/Local/daysaver/save`
- macOS: `~/Library/Application Support/daysaver/save`
- Linux: `~/.local/share/daysaver/save`
