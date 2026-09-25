# SteamEmbed

Discord bot that detects SteamIDs and Steam vanity URLs in messages (including embeds) and replies with links to their profiles on [steamid.zmod.gg](https://steamid.zmod.gg/).

Ported from the `onmessage` module of lamarr-discord.

## Supported formats

- SteamID2: `STEAM_0:1:123456`
- SteamID3: `[U:1:249153]`
- SteamID64: `76561198000123456`
- Vanity URLs: `https://steamcommunity.com/id/gabelogannewell`

## Setup

```bash
pip install -r requirements.txt
copy .env.example .env  # then put your bot token in DISCORD_TOKEN
python main.py
```

The bot needs the `message_content` intent enabled in the Discord developer portal.