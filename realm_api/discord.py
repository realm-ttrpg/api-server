# 3rd party
from aiohttp import ClientSession


class DiscordClient:
    user_id: str
    token: str

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    async def api(self, url):
        async with ClientSession() as http:
            http.headers.add("Authorization", f"Bearer {self.token}")

            async with http.get(
                f"https://discord.com/api/v10{url}"
            ) as response:
                return await response.json()

    async def get_user_info(self):
        return await self.api("/oauth2/@me")

    async def get_guilds(self):
        return await self.api("/users/@me/guilds")
