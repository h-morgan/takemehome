# takemehome
Desktop app for Take Me Home software


## Development

To run the project during development:
```bash
poetry run python takemehome/main.py
```

## Build

To build the executable with PyInstaller: First, export the Poetry environment:
```bash
poetry export -f requirements.txt --output requirements.txt
```

Then build the executable:
```bash
pyinstaller --onefile --noconsole --name takemehome takemehome/main.py
```