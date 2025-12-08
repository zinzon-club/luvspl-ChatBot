from fastapi import FastAPI, Request
from dotenv import load_dotenv
from ai_service import analyze_sentence

load_dotenv()
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/bot")
async def bot(request: Request):

    # JSON 안전하게 파싱
    try:
        body = await request.json()
    except Exception:
        body = {}

    user_request = body.get("userRequest", {})
    utterance = user_request.get("utterance", "")

    # 유효성 검사
    if not utterance:
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": "⚠️ 문장을 다시 입력해줘!"}}
                ]
            }
        }

    # AI 분석
    answer = await analyze_sentence(utterance)

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": answer}}
            ]
        }
    }
