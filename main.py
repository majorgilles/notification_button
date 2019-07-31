from fastapi import FastAPI
from gpiozero import LED
from gpiozero.exc import BadPinFactory, GPIOPinInUse
from starlette.websockets import WebSocket

app = FastAPI()
led = LED(17)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data.get("activate") is True:
            if not led.is_active:
                led.on()
            await websocket.send_json({"success": True, "message": "The light was activated"})
