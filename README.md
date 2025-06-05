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

To convert this game into an Android APK you can use Kivy's Buildozer tool:

1. Install buildozer and its dependencies.
2. Initialize a spec file:
   ```bash
   buildozer init
   ```
3. Edit the generated `buildozer.spec` to include `pygame` and your entry
   point (`run_game.py`).
4. Build the APK:
   ```bash
   buildozer -v android debug
   ```

For more details see the Buildozer documentation.
