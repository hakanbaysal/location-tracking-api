import asyncio
import json
from datetime import datetime


async def send_data(host, port, data):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        message = json.dumps(data).encode()

        writer.write(message)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print("Data sent successfully.")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    example_data = {
        "device_id": "test_device",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 60.0,
        "timestamp": datetime.now().isoformat()
    }
    asyncio.run(send_data("127.0.0.1", 5001, example_data))
