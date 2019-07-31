from fastapi import FastAPI
from gpiozero import LED
from starlette.websockets import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data.get("activate") is True:
            led = LED(17)
            led.on()
            await websocket.send_json({"success": True})
