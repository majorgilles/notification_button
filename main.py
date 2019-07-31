from fastapi import FastAPI
from gpiozero import LED
from gpiozero.exc import BadPinFactory, GPIOPinInUse
from starlette.websockets import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data.get("activate") is True:
            message = turn_led_on()
            await websocket.send_json(message)


def turn_led_on():
    try:
        led = LED(17)
        if not led.is_active:
            led.on()
    except BadPinFactory:
        return {"success": False, "message": "The current device does not support GPIO operations"}
    except GPIOPinInUse:
        pass

    return {"success": True, "message": "The light was turned on"}
