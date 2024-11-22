import asyncio
import json
from datetime import datetime
from celery_tasks.location_tasks import process_location
from config.settings import settings

class LocationTCPController:
    async def handle_client(self, reader, writer):
        try:
            data = await reader.read(1024)
            message = data.decode()
            location_data = json.loads(message)
            location_data["source"] = "tcp"
            location_data["timestamp"] = datetime.fromisoformat(location_data["timestamp"]) if isinstance(location_data["timestamp"], str) else datetime.now()
            process_location.delay(location_data)
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"Error handling client: {e}")

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client,
            settings.TCP_HOST,
            settings.TCP_PORT
        )
        print(f"TCP Server running on {settings.TCP_HOST}:{settings.TCP_PORT}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    controller = LocationTCPController()
    asyncio.run(controller.start_server())
