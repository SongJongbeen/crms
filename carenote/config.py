import os

# 프로젝트 루트 디렉토리
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 데이터베이스 경로
DB_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DB_DIR, 'carenote.db')

# 데이터베이스 디렉토리가 없으면 생성
os.makedirs(DB_DIR, exist_ok=True)
