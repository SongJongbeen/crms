"""데이터베이스 연결 및 초기화"""
import sqlite3
from carenote.config import DB_PATH


def get_connection():
    """데이터베이스 연결 반환"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Foreign key 활성화
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn


def init_database():
    """데이터베이스 테이블 초기화"""
    conn = get_connection()
    cursor = conn.cursor()

    # students 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_phone TEXT,
            student_grade INTEGER CHECK(student_grade IN (1,2,3,4,5,6)),
            student_class INTEGER CHECK(student_class IN (1,2,3,4)),
            student_sex TEXT CHECK(student_sex IN ('남','여')),
            student_history TEXT DEFAULT '[]'
        )
    """)

    # consultings 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultings (
            consulting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulting_title TEXT NOT NULL,
            consulting_date TEXT DEFAULT (datetime('now','localtime')),
            student_id INTEGER NOT NULL,
            consulting_type TEXT CHECK(consulting_type IN ('전화','대면','기타')),
            consulting_object TEXT CHECK(consulting_object IN ('본인','가족','교사','기타')),
            consulting_content TEXT,
            consulting_opinion TEXT,
            consulting_note TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        )
    """)

    # 인덱스 생성
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_consultings_student 
        ON consultings(student_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_consultings_date 
        ON consultings(consulting_date)
    """)

    conn.commit()
    conn.close()
    print(f"데이터베이스 초기화 완료: {DB_PATH}")
