"""메인 실행 파일"""
from carenote.database import init_database
from carenote.cli import main_menu


if __name__ == "__main__":
    # 데이터베이스 초기화
    init_database()

    # CLI 실행
    main_menu()
