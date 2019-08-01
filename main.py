from fastapi import FastAPI
from starlette.websockets import WebSocket

from notification_manager import NotificationManager

app = FastAPI()
notification_manager = NotificationManager(17, 18)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()

        if data.get("activate"):
            notification_manager.notify()
            await websocket.send_json({"success": True, "message": "The light was activated"})
