from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from vosk import Model, KaldiRecognizer
from websocket_connection.connection_manager import ConnectionManager
import base64
import json


MODEL_PATH = "ml_models/vosk"
SAMPLE_RATE = 16000


router = APIRouter()

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

manager = ConnectionManager()


@router.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    
    await manager.connect(websocket)

    try:

     while True:
        data = await websocket.receive_text()
        message = json.loads(data)

        if message.get("type") == "audio":
            pcm_data = base64.b64decode(message.get("data"))
            ok = recognizer.AcceptWaveform(pcm_data)

            if ok:
                result = json.loads(recognizer.Result())
                await websocket.send_json({
                    "type": "final",
                    "text": result.get("text", "")
                })
            else:
                partial = json.loads(recognizer.PartialResult())
                await websocket.send_json({
                    "type": "partial",
                    "text": partial.get("partial", "")
                })

        if message.get("type") == "eof":
            final = json.loads(recognizer.FinalResult())
            await websocket.send_json({
                "type": "final",
                "text": final.get("text", "")
            })
            break

    except WebSocketDisconnect:
        manager.disconnect(websocket)