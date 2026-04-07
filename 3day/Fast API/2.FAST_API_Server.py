# ==========================================
# FastAPI 서버 예제 (server_fastapi.py)
# ==========================================
# 기능:
# - 클라이언트가 POST로 텍스트 데이터를 보내면
# - 서버가 분석(문자 길이 계산) 후 결과를 반환함
# ==========================================

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# ------------------------------------------
# 1. 데이터 모델 정의
# ------------------------------------------
class TextData(BaseModel):
    text: str  # 클라이언트에서 보낼 데이터 구조 정의

# ------------------------------------------
# 2. FastAPI 인스턴스 생성
# ------------------------------------------
app = FastAPI(
    title="FastAPI 서버 예제",
    description="클라이언트와 데이터 송수신하는 기본 예제",
    version="1.0.0"
)

# ------------------------------------------
# 3. 기본 확인용 GET 엔드포인트
# ------------------------------------------
@app.get("/")
def home():
    """
    서버 상태를 확인하는 기본 GET 엔드포인트.
    """
    return {"message": " FastAPI 서버가 정상적으로 실행 중입니다!"}

# ------------------------------------------
# 4. POST 요청 처리 (텍스트 분석)
# ------------------------------------------
@app.post("/analyze")
def analyze_text(data: TextData):
    """
    클라이언트로부터 텍스트를 받아 길이 분석 결과 반환
    요청 JSON 예시:
    {
        "text": "AI 기반 프레스 설비 테스트 중입니다."
    }
    """
    text = data.text
    length = len(text)
    word_count = len(text.split())

    result = {
        "original_text": text,
        "char_length": length,
        "word_count": word_count,
        "message": f"문자 수 {length}개, 단어 수 {word_count}개 분석 완료 "
    }

    return result

# ------------------------------------------
# 5. FastAPI 서버 실행
# ------------------------------------------
if __name__ == "__main__":
    # uvicorn으로 FastAPI 실행
    # host='192.168.99.2', port=8000 은 기본 로컬 서버 주소
    uvicorn.run(app, host="192.168.99.2", port=8000)
