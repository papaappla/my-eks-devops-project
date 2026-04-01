FROM python:3.11-slim

WORKDIR /app

# 인코딩 설정 추가 (한글 처리 지원)
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# 1. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 모든 소스 코드 복사 (main.py, reporter.py 등)
COPY . .

# 3. 기본 실행은 main.py (FastAPI 서버)
# CronJob에서는 'python reporter.py'로 오버라이드하여 실행합니다.
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
