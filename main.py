from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from schemas import KakaoRequest
from ai_service import analyze_sentence

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/bot")
async def analyze(req: KakaoRequest):
    if not req.userRequest:
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": "⚠️ userRequest를 찾을 수 없습니다."}}
                ]
            }
        }

    utterance = req.userRequest.get("utterance")

    if not utterance:
        answer = "⚠️ 문장을 인식하지 못했습니다. 다시 입력해주세요!"
    else:
        answer = await analyze_sentence(utterance)

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": answer}}
            ]
        }
    }