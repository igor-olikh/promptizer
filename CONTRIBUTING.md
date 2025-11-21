# Contributing to Promptizer

Thank you for your interest in contributing to Promptizer! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Error messages or logs (if applicable)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use cases and examples
- Potential implementation approach (if you have ideas)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure code follows the existing style
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/igor-olikh/promptizer.git
   cd promptizer
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env and add your keys
   ```

4. Run tests (when available):
   ```bash
   poetry run pytest
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

