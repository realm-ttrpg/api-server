# Realm TTRPG API server

An API server for use with the associated [bot software][] and
[web interface][] to facilitate the play and administration of
[tabletop roleplaying games][]

![realm](https://raw.githubusercontent.com/realm-ttrpg/api-server/assets/banner.jpg)

## Installing

First, make a `config.toml` file from the provided `config.example.toml` file,
providing it with any settings tweaks you wish to apply.

Then, install the server package in your Python environment of choice:

```shell
pip install -U 'realm_api@git+https://github.com/realm-ttrpg/api-server.git'
```

## Running

In the same directory as your `config.toml` file:

```shell
python -m aethersprite.webapp
```

[bot software]: https://github.com/realm-ttrpg/discord-bot
[tabletop roleplaying games]: https://en.wikipedia.org/wiki/Tabletop_role-playing_game
[web interface]: https://github.com/realm-ttrpg/web-interface
