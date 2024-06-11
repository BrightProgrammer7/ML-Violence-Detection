import requests
from fastapi import FastAPI, File, UploadFile, HTTPException

url = "http://127.0.0.1:8000/detect_violence"
app = FastAPI()

@app.get("/detect")
async def detect():
    files = {"video_file": open("V_19.mp4", "rb")}
    response = requests.post(url, files=files)

    print(response.text)
    return {"response": response.text}
    
