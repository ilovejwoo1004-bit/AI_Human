# ==========================
# AI 서버 (FastAPI 기반)
# ==========================
# 클라이언트로부터 분석 요청(JSON)을 받아
# 감정 분석, 텍스트 길이 분석, 키워드 탐지 결과를 반환하는 예제입니다.
# 실행 후 http://192.168.99.2:8000/docs 에서 테스트 가능
# ==========================

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# -----------------------------------
# 1. 감성 분석 모델 로드
# -----------------------------------
# Hugging Face의 사전 학습된 모델을 사용
# 최초 로드 시 약 400~500MB 다운로드가 발생 (1회만).
sentiment_analyzer = pipeline("sentiment-analysis")

# -----------------------------------
# 2. FastAPI 앱 생성
# -----------------------------------
app = FastAPI(title="AI 분석 서버")

# -----------------------------------
# 3. 요청 데이터 구조 정의 (Pydantic)
# -----------------------------------
# 클라이언트가 보낸 JSON 데이터를 자동 검증 및 파싱.
class AnalysisRequest(BaseModel):
    mode: str  # 분석 모드 (length / sentiment / keyword)
    text: str  # 분석할 문장

# -----------------------------------
# 4. 분석 API 엔드포인트 정의
# -----------------------------------
@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    # 요청값 읽기
    mode = request.mode.lower()
    text = request.text

    # -----------------------------------
    # (1) 문장 길이 분석
    # -----------------------------------
    if mode == "length":
        result = {
            "result": len(text),
            "desc": f"문장 길이는 {len(text)}자입니다."
        }

    # -----------------------------------
    # (2) 감성 분석 (transformers 이용)
    # -----------------------------------
    elif mode == "sentiment":
        # 감성 분석 모델 호출
        analysis = sentiment_analyzer(text)[0]
        label = analysis['label']      # 감정 결과 (POSITIVE/NEGATIVE)
        score = round(analysis['score'], 3)  # 신뢰도 (0~1)
        result = {
            "result": label,
            "confidence": score,
            "desc": f"감정: {label}, 신뢰도: {score}"
        }

    # -----------------------------------
    # (3) 키워드 탐지
    # -----------------------------------
    elif mode == "keyword":
        # 간단히 지정된 키워드 리스트를 문장 안에서 탐색
        keywords = ["AI", "press", "factory", "defect", "data", "불량"]
        found = [w for w in keywords if w.lower() in text.lower()]
        result = {
            "result": found,
            "desc": f"키워드 발견: {', '.join(found) if found else '없음'}"
        }

    # -----------------------------------
    # (4) 지원하지 않는 모드 처리
    # -----------------------------------
    else:
        result = {"error": f"지원하지 않는 모드입니다: {mode}"}

    # 결과 JSON 반환
    return result

# -----------------------------------
# 5. 서버 실행부
# -----------------------------------
# uvicorn 내장 서버를 이용해 FastAPI 앱 실행
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.7", port=8000)



