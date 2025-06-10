# Flying Bird

This project provides a minimal Flappy Bird style game written in Python using
Pygame. You can run it on desktop platforms and later package it as an Android
APK using tools such as [Pygame Subset for Android](https://github.com/renpy/pygame_sdl2) or [Kivy's Buildozer](https://github.com/kivy/buildozer).

## Running the Game

1. Install Python 3.x.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python run_game.py
   ```

Press `SPACE` to jump. Avoid the pipes! Press `R` after a crash to restart.

## Packaging for Android

To convert this game into an Android APK you can use Kivy's Buildozer tool.
Below is a minimal workflow tested on Ubuntu Linux:

1. Install the required system packages:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip openjdk-17-jdk unzip git build-essential ccache libncurses5
   pip3 install --user buildozer
   ```
2. If you are running Python 3.12 or newer execute Buildozer via the provided
   wrapper to ensure the `distutils` module is available:
   ```bash
   python buildozer_wrapper.py init
   ```
   Otherwise you can call `buildozer init` directly.
3. Edit the generated `buildozer.spec` so that `requirements` contains
   `pygame` and ensure `source.main` points to `main.py` (already done in this
   repository).
4. Build the APK:
   ```bash
   python buildozer_wrapper.py -v android debug
   ```

The resulting APK will be placed in the `bin/` directory. Install it on your
device via `adb install bin/*.apk` or through Android's file manager.

### Building with GitHub Actions

This repository includes a workflow that automatically builds an APK using [Buildozer](https://github.com/kivy/buildozer) when you push changes to the `main` branch or open a pull request. The generated APK is uploaded as a workflow artifact.

To trigger the workflow manually, push your commits to GitHub and check the *Actions* tab. Once the build completes you can download the APK artifact from the workflow run page.
