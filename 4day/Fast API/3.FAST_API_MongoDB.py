# ==========================================
# FastAPI + MongoDB 연동 예제
# ==========================================
# 기능:
# 1. 클라이언트가 POST로 데이터를 보내면 MongoDB에 저장
# 2. GET 요청으로 저장된 데이터를 조회
# ==========================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from pymongo import MongoClient
from bson import ObjectId  # MongoDB ObjectId 처리용
import json

# ----------------------------------------
# 1. MongoDB 연결 설정
# ----------------------------------------
MONGO_URL = "mongodb://localhost:27017/"  # 로컬 MongoDB
DB_NAME = "fastapi_db"
COLLECTION_NAME = "items"

# MongoClient 생성
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ----------------------------------------
# 2. FastAPI 앱 생성
# ----------------------------------------
app = FastAPI(
    title="FastAPI MongoDB 실습 예제",
    description="클라이언트 요청을 MongoDB에 자동 저장하고 조회",
    version="1.0.0"
)

# ----------------------------------------
# 3. Pydantic 데이터 모델 정의
# ----------------------------------------
class Item(BaseModel):
    name: str                # 필수: 아이템 이름
    price: float             # 필수: 가격
    description: Optional[str] = None  # 선택: 설명

# ----------------------------------------
# 4. ObjectId → str 변환 헬퍼 함수
# ----------------------------------------
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# ----------------------------------------
# 5. POST 요청: MongoDB에 데이터 저장
# ----------------------------------------
@app.post("/items")
def create_item(item: Item):
    """
    클라이언트가 보낸 JSON 데이터를 MongoDB에 저장
    """
    # MongoDB 문서 생성
    item_dict = item.dict()
    result = collection.insert_one(item_dict)  # DB에 저장

    # 저장된 문서 ID 반환
    return {
        "message": f"{item.name} 저장 완료 ",
        "id": str(result.inserted_id)
    }

# ----------------------------------------
# 6. GET 요청: MongoDB 데이터 조회
# ----------------------------------------
@app.get("/items", response_model=List[Item])
def get_items():
    """
    MongoDB에 저장된 모든 아이템 조회
    """
    items = list(collection.find({}))  # 모든 문서 조회
    # ObjectId 변환 후 반환
    return json.loads(JSONEncoder().encode(items))

# ----------------------------------------
# 7. FastAPI 서버 실행
# ----------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.99.2", port=8000)
