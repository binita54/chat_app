import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/general?token=your_token_here"
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")

        # Send 5 messages with 1 second interval
        for i in range(5):
            message = f"Message {i+1} from client!"
            await websocket.send(json.dumps({"content": message}))
            print(f"✅ Sent: {message}")
            await asyncio.sleep(1)

        try:
            while True:
                response = await websocket.recv()
                print("📩 Received:", response)
        except websockets.ConnectionClosed as e:
            print("❌ Connection closed:", e)

asyncio.run(test_ws())
