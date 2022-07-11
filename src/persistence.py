from typing import Dict
import aioredis
from telegram.ext import DictPersistence


class RedisPersistence(DictPersistence):

    def __init__(self, *args,  redis_url: str, key_prefix: str = 'bot', **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = aioredis.from_url(redis_url, decode_responses=True)
        self.key_prefix = key_prefix

    async def refresh_user_data(self, user_id: int, user_data: Dict) -> None:
        if not user_data:
            data = await self.redis_client.hgetall(f"{self.key_prefix}:user:{user_id}")
            user_data.update(data)

    async def update_user_data(self, user_id: int, data: Dict) -> None:
        await self.redis_client.hset(
            name=f"{self.key_prefix}:user:{user_id}",
            mapping=data)

    async def flush(self) -> None:
        for user_id, data in self.user_data.items():
            await self.redis_client.hset(
                name=f"{self.key_prefix}:user:{user_id}",
                mapping=data)
        await self.redis_client.close()
        await self.redis_client.connection_pool.disconnect()
