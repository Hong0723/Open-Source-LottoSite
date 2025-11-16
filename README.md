# 1. 저장소 클론
git clone https://github.com/사용자명/lotto-site.git
cd lotto-site

# 2. (선택) 가상환경 생성 및 활성화 – 로컬 실행 시
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# 3. Docker Compose로 컨테이너 실행
docker compose up -d --build

# 4. Django 마이그레이션 및 관리자 계정 생성
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
