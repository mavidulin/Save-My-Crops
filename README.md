Save My Crops

---

Development Notes:

Enable jpeg with django files widget or similar:

Without jpeg library installed on system pillow can't provide jpeg support.

Before installing django requirements install jpeg library:

```sudo apt-get install libjpeg-dev``` 

If you already installed pillow, install jpeg library and reinstall pillow:

```sudo apt-get install libjpeg-dev```

```pip install -I pillow```
