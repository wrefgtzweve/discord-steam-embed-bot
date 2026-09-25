import interactions
import re
from interactions.api.events import MessageCreate

steamid_site = r"https://steamid.zmod.gg/"
steamid_pattern = re.compile(r'STEAM_[0-5]:[01]:\d+|\[U:1:\d+\]|7656119\d{10}')
steamid_lookup = r"https://steamid.zmod.gg/lookup?q="
vanity_url_pattern = re.compile(r'https?://steamcommunity\.com/id/([A-Za-z0-9_-]+)')
whitelisted_bots = set()


def to_steamid64(steamid):
    base = 76561197960265728
    if steamid.startswith("STEAM_"):  # SteamID2
        parts = steamid.split(':')
        if len(parts) != 3 or not parts[2].isdigit():
            raise ValueError("Invalid SteamID2 format")
        y = int(parts[1])  # Account type
        z = int(parts[2])  # Account number
        return str((z * 2) + y + base)
    elif steamid.startswith("[U:1:"):  # SteamID3
        z = int(steamid.strip("[]").split(":")[2])
        return str(z + base)
    elif steamid.isdigit() and len(steamid) == 17 and steamid.startswith("7656119"):  # SteamID64
        return steamid
    else:
        return False


class SteamEmbed(interactions.Extension):
    @interactions.listen(MessageCreate)
    async def on_message(self, event: MessageCreate):
        if event.message.author == event.client.user:
            return

        if event.message.author.bot and event.message.author.id not in whitelisted_bots:
            return

        message_text = event.message.content
        for embed in event.message.embeds:
            if embed.description:
                message_text += embed.description

            if embed.title:
                message_text += embed.title

            for field in embed.fields:
                message_text += field.name + field.value

        if message_text == "":
            return

        vanity_matches = vanity_url_pattern.findall(message_text)
        if vanity_matches:
            message = ""

            # Deduplicate matches
            vanity_matches = list(set(vanity_matches))

            for match in vanity_matches:
                message += f"{steamid_lookup}{match}\n"
            message = message[:-1]
            await event.message.reply(message, silent=True, allowed_mentions=interactions.AllowedMentions.none())

        steamid_text = message_text.replace("\\_", "_")
        matches = steamid_pattern.findall(steamid_text)
        if matches:
            message = ""

            # Deduplicate matches
            matches = list(set(matches))

            for match in matches:
                steamid64 = to_steamid64(match)
                if steamid64:
                    message += f"[{match}]({steamid_site}{steamid64})\n"
            if message:
                message = message[:-1]
                await event.message.reply(message, silent=True, allowed_mentions=interactions.AllowedMentions.none())