# ==========================
# AI TCP/IP 클라이언트 예제
# ==========================
# 사용자가 선택한 분석 조건(mode)과 텍스트를 입력하면,
# 이를 JSON 형태로 AI 서버에 전송하고 분석 결과를 받아 출력합니다.
# ==========================

import socket  # TCP 통신용
import json    # JSON 직렬화/역직렬화용

# -----------------------------------
# 1. 서버 접속 설정
# -----------------------------------
HOST = '192.168.0.174'  # 서버 IP 주소
PORT = 9999         # 서버 포트 번호 (서버 코드와 동일해야 함)

# -----------------------------------
# 2. TCP 소켓 생성 및 서버 연결
# -----------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("AI 서버에 연결되었습니다. (종료하려면 'exit' 입력)\n")

# -----------------------------------
# 3. 사용자 입력 및 요청 전송 루프
# -----------------------------------
while True:
    # 분석 모드 입력
    mode = input("분석 모드 입력 (length / sentiment / keyword): ").strip()

    # 종료 명령 시 서버에 exit 전송 후 종료
    if mode.lower() == "exit":
        client_socket.sendall(mode.encode())
        print("클라이언트 종료 중...")
        break

    # 분석할 텍스트 입력
    text = input("분석할 문장 입력: ").strip()

    # -----------------------------------
    # 4. 요청 데이터(JSON) 구성
    # -----------------------------------
    request = {
        "mode": mode,
        "text": text
    }

    # JSON → 문자열 → bytes 인코딩 후 전송
    client_socket.sendall(json.dumps(request, ensure_ascii=False).encode())

    # -----------------------------------
    # 5. 서버 응답 수신
    # -----------------------------------
    data = client_socket.recv(2048).decode()

    try:
        # 수신한 JSON 문자열을 dict로 변환
        response = json.loads(data)
        print(f"\n 서버 분석 결과:\n{json.dumps(response, ensure_ascii=False, indent=2)}\n")
    except json.JSONDecodeError:
        print(f" 서버 응답 형식 오류: {data}\n")

# -----------------------------------
# 6. 소켓 닫기
# -----------------------------------
client_socket.close()
print(" 클라이언트 종료 완료")
