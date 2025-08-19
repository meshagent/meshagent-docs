from meshagent.api.webhooks import WebhookServer, RoomStartedEvent, RoomEndedEvent
import asyncio


class CustomWebhookServer(WebhookServer):
    async def on_room_started(self, event: RoomStartedEvent):
        print(f"room started {event.room_name}")
        pass

    async def on_room_ended(self, event: RoomEndedEvent):
        print(f"room ended {event.room_name}")
        pass


async def main():
    server = CustomWebhookServer()
    await server.run()


asyncio.run(main())
