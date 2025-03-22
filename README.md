# takemehome
Desktop app for Take Me Home software


## Development

To run the project during development:
```bash
poetry run python takemehome/main.py
```

## Build

To build the executable with PyInstaller, use the following command to create a standalone `.app` bundle
```bash
poetry run pyinstaller --name "Take Me Home" --windowed --add-data "people.db:." --onefile takemehome/main.py
```

Next, run the application by running:
```bash
./dist/Take\ Me\ Home.app/Contents/MacOS/Take\ Me\ Home
```

To package the application for distribution (creates a .dmg file), run:

```bash
create-dmg \
  --volname "Take Me Home Installer" \
  --window-pos 200 200 \
  --window-size 500 300 \
  --icon-size 100 \
  --app-drop-link 400 150 \
  "dist/Take Me Home Installer.dmg" "dist/Take Me Home.app"
```
On a Mac, this will open a window that will allow you to drag the "Take Me Home" application into the "Applications" folder.

To clean house and start fresh, run:
```bash
rm -rf dist build "Take Me Home.spec"
```