# ==============================
# FastAPI 기본 실습 예제
# ==============================
# 기능:
# 1. GET 요청 → 서버 상태 확인
# 2. POST 요청 → 사용자 데이터를 받아 처리 후 응답
# ==============================

# FastAPI 프레임워크 임포트
from fastapi import FastAPI
from pydantic import BaseModel  # 입력 데이터 유효성 검사용
from typing import Optional

# ----------------------------------------
# 1. FastAPI 앱 인스턴스 생성
# ----------------------------------------
# app 객체는 서버의 중심이며, 모든 API 엔드포인트를 여기에 등록함
app = FastAPI(
    title="FastAPI 기본 예제",
    description="PyCharm에서 실습 가능한 FastAPI 기본 예제",
    version="1.0.0"
)

# ----------------------------------------
# 2. 데이터 모델 정의 (POST 요청 시)
# ----------------------------------------
class Item(BaseModel):
    name: str                # 필수: 아이템 이름
    price: float             # 필수: 가격
    description: Optional[str] = None  # 선택: 설명

# ----------------------------------------
# 3. 기본 엔드포인트 (GET 요청)
# ----------------------------------------
# URL: http://192.168.99.2:8000/
@app.get("/")
def read_root():
    """
    서버 상태 확인용 기본 엔드포인트.
    브라우저나 curl로 GET 요청 시 메시지 반환.
    """
    return {"message": "FastAPI 서버가 정상적으로 동작 중입니다!"}

# ----------------------------------------
# 4. 단순 GET 요청 예제 (Query Parameter 사용)
# ----------------------------------------
# URL 예시: http://192.168.99.2:8000/hello?name=현석
@app.get("/hello")
def say_hello(name: str = "사용자"):
    """
    GET 요청 시 URL 파라미터로 이름을 받아 인사 메시지를 반환
    예) /hello?name=홍길동
    """
    return {"message": f"안녕하세요, {name}님! "}

# ----------------------------------------
# 5. POST 요청 예제 (Body 데이터 받기)
# ----------------------------------------
# URL: http://192.168.99.2:8000/items
@app.post("/items")
def create_item(item: Item):
    """
    JSON 형식의 데이터를 수신하여 서버에서 처리 후 결과 반환.
    POST 요청 예시(JSON Body):
    {
        "name": "노트북",
        "price": 1500000,
        "description": "AI 모델 학습용 고성능 노트북"
    }
    """
    # 간단한 로직: 부가세 계산
    total_price = item.price * 1.1

    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "total_with_tax": total_price,
        "message": f"{item.name} 상품이 성공적으로 등록되었습니다!"
    }

# ----------------------------------------
# 6. FastAPI 실행 (uvicorn)
# ----------------------------------------
# PyCharm에서 직접 실행하려면 아래 코드 블록을 그대로 두세요.
# 터미널에서 실행 시: uvicorn fastapi_basic:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.99.2", port=8000)
