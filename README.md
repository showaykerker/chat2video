# vid-from-discord

A script that can easily make screenshots of chat into video (with sounds!).

## Usage
1. Create a folder `images`, put screenshots inside with names `img#.jpg`
2. Copy `example.config.json` to `config.json` and modify the configuration.
3. Get the sound effect of discord and name it `discord-notification.mp3`
4. Create venv and install requirements.txt
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
5. Run the script
```bash
(venv) $ python main.py
```

## TODO
- [] Complete README.md
- [] Support for multiple sound effect
- [] Add demo video
- [] Release binary version
- [] More configuration!

