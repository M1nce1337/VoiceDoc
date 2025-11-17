from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from vosk import Model, KaldiRecognizer
from typing import List
import base64
import json

MODEL_PATH = "vosk-model-small-ru-0.22"
SAMPLE_RATE = 16000

app = FastAPI(
    title="Real-Time Audio Processor",
    description="Process and transcribe audio in real-time using Vosk"
)
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)        

manager = ConnectionManager()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/audio")
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