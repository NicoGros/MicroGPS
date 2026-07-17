# Contributing to MicroGPS

Thank you for your interest in improving MicroGPS.

## Reporting issues

Please use the GitHub issue tracker.

When reporting a bug, include:

- MicroGPS version
- steps to reproduce
- screenshots if relevant

I will try to help as much as I can :)

## Development

Clone the repository:

```bash
git clone https://github.com/<username>/MicroGPS.git
cd MicroGPS
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application from the repository root:

```bash
python run.py
```

Alternatively, if running directly from the package:

```bash
python -m MicroGPS.main
```

## Coding style

- I am not a developer myself, you may find the style not optimal.
- Use descriptive names.
- Add docstrings for classes and functions.
- Keep GUI logic separated from application logic.

## Pull requests

- keep pull requests focused on one feature or fix.
- explain the motivation.
- ensure the application starts correctly before submitting.
