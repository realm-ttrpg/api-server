# Realm TTRPG API server

An API server for use with the associated [bot software][] and
[web interface][] to facilitate the play and administration of
[tabletop roleplaying games][]

![realm](https://raw.githubusercontent.com/realm-ttrpg/api-server/assets/banner.jpg)

## Installing

Install the server package in your Python environment of choice:

```shell
pip install -U 'realm_api@git+https://github.com/realm-ttrpg/api-server.git'
```

## Running

```shell
python -m realm_api
```

## Configuration

Settings are available via the following environment variables:

- `DB_URL` - Postgres connection string
- `REALM_HOST` - Hostname/IP to bind to
- `REALM_PORT` - Port to bind to
- `REDIS_HOST` - Hostname for redis server

[bot software]: https://github.com/realm-ttrpg/discord-bot
[tabletop roleplaying games]: https://en.wikipedia.org/wiki/Tabletop_role-playing_game
[web interface]: https://github.com/realm-ttrpg/web-interface
