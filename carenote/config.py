import os
import sys

# PyInstaller로 빌드된 경우와 일반 실행 환경 모두 지원
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 경우: exe 파일이 있는 디렉토리
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 일반 Python 실행 환경: 프로젝트 루트 디렉토리
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 데이터베이스 경로
DB_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DB_DIR, 'carenote.db')

# 데이터베이스 디렉토리가 없으면 생성
os.makedirs(DB_DIR, exist_ok=True)
