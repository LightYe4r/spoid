FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt /app/

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# 명령어 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
