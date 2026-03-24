# 기존: FROM python:3.9-slim
# 변경:
FROM python:3.11-slim

WORKDIR /app

# (이하 동일)
COPY requirements.txt .

# 3. 필요한 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY main.py .

# 5. API 포트 개방 및 실행
EXPOSE 8000
CMD ["python", "main.py"]
