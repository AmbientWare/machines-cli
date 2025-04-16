# machines-cli

A command-line interface tool for managing and interacting with machines, built with Python and Typer.

## Features

- SSH configuration management
- Machine management and operations
- Configuration handling
- Logging capabilities
- API integration

## Requirements

- Python 3.12 or higher
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/machines-cli.git
cd machines-cli
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

The CLI tool is available as `lazycloud` after installation. Here are some basic commands:

```bash
# Get help
lazycloud --help

# List available commands
lazycloud --help-commands
```

## Development

This project uses Poetry for dependency management and packaging. The main components are:

- `machines_cli/commands/`: CLI command implementations
- `machines_cli/api/`: API integration code
- `machines_cli/config.py`: Configuration management
- `machines_cli/ssh_config.py`: SSH configuration handling
- `machines_cli/logging.py`: Logging functionality

## Dependencies

- pydantic: Data validation
- pydantic-settings: Settings management
- httpx: HTTP client
- typer: CLI framework
