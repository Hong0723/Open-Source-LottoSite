FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 & MySQL client 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# requirements 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

# Django 서버 실행 명령 (포트 8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
