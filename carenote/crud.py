"""CRUD 작업"""
import json
from typing import List, Optional
from carenote.database import get_connection
from carenote.models import Student, Consulting


class StudentCRUD:
    """학생 CRUD 작업"""

    @staticmethod
    def create(student: Student) -> int:
        """학생 생성"""
        conn = get_connection()
        cursor = conn.cursor()

        data = student.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])

        cursor.execute(
            f"INSERT INTO students ({columns}) VALUES ({placeholders})",
            tuple(data.values())
        )

        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return student_id

    @staticmethod
    def get(student_id: int) -> Optional[Student]:
        """학생 조회"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Student(**dict(row))
        return None

    @staticmethod
    def get_all() -> List[Student]:
        """모든 학생 조회"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY student_name")
        rows = cursor.fetchall()
        conn.close()

        return [Student(**dict(row)) for row in rows]

    @staticmethod
    def update(student_id: int, **kwargs):
        """학생 정보 업데이트"""
        conn = get_connection()
        cursor = conn.cursor()

        # 현재 학년/반 정보 가져오기 (히스토리 업데이트용)
        if 'student_grade' in kwargs or 'student_class' in kwargs:
            cursor.execute(
                "SELECT student_grade, student_class, student_history FROM students WHERE student_id = ?",
                (student_id,)
            )
            row = cursor.fetchone()
            if row:
                current_grade = row['student_grade']
                current_class = row['student_class']
                history = json.loads(row['student_history']) if row['student_history'] else []

                # 현재 정보를 히스토리에 추가
                if current_grade and current_class:
                    history.append({"grade": current_grade, "class": current_class})
                    kwargs['student_history'] = json.dumps(history, ensure_ascii=False)

        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (student_id,)

        cursor.execute(
            f"UPDATE students SET {set_clause} WHERE student_id = ?",
            values
        )

        conn.commit()
        conn.close()

    @staticmethod
    def delete(student_id: int):
        """학생 삭제 (연결된 상담 기록도 자동 삭제)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(name: str = None, grade: int = None, class_num: int = None) -> List[Student]:
        """학생 검색"""
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if name:
            query += " AND student_name LIKE ?"
            params.append(f"%{name}%")
        if grade:
            query += " AND student_grade = ?"
            params.append(grade)
        if class_num:
            query += " AND student_class = ?"
            params.append(class_num)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [Student(**dict(row)) for row in rows]


class ConsultingCRUD:
    """상담 CRUD 작업"""

    @staticmethod
    def create(consulting: Consulting) -> int:
        """상담 기록 생성"""
        conn = get_connection()
        cursor = conn.cursor()

        data = consulting.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])

        cursor.execute(
            f"INSERT INTO consultings ({columns}) VALUES ({placeholders})",
            tuple(data.values())
        )

        consulting_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return consulting_id

    @staticmethod
    def get(consulting_id: int) -> Optional[Consulting]:
        """상담 기록 조회"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultings WHERE consulting_id = ?", (consulting_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Consulting(**dict(row))
        return None

    @staticmethod
    def get_by_student(student_id: int) -> List[Consulting]:
        """특정 학생의 모든 상담 기록 조회"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM consultings WHERE student_id = ? ORDER BY consulting_date DESC",
            (student_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [Consulting(**dict(row)) for row in rows]

    @staticmethod
    def get_all() -> List[Consulting]:
        """모든 상담 기록 조회"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultings ORDER BY consulting_date DESC")
        rows = cursor.fetchall()
        conn.close()

        return [Consulting(**dict(row)) for row in rows]

    @staticmethod
    def update(consulting_id: int, **kwargs):
        """상담 기록 업데이트"""
        conn = get_connection()
        cursor = conn.cursor()

        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (consulting_id,)

        cursor.execute(
            f"UPDATE consultings SET {set_clause} WHERE consulting_id = ?",
            values
        )

        conn.commit()
        conn.close()

    @staticmethod
    def delete(consulting_id: int):
        """상담 기록 삭제"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultings WHERE consulting_id = ?", (consulting_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(title: str = None, student_name: str = None, 
               consulting_type: str = None, start_date: str = None, end_date: str = None) -> List[Consulting]:
        """상담 기록 검색"""
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT c.* FROM consultings c
            JOIN students s ON c.student_id = s.student_id
            WHERE 1=1
        """
        params = []

        if title:
            query += " AND c.consulting_title LIKE ?"
            params.append(f"%{title}%")
        if student_name:
            query += " AND s.student_name LIKE ?"
            params.append(f"%{student_name}%")
        if consulting_type:
            query += " AND c.consulting_type = ?"
            params.append(consulting_type)
        if start_date:
            query += " AND c.consulting_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND c.consulting_date <= ?"
            params.append(end_date)

        query += " ORDER BY c.consulting_date DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [Consulting(**dict(row)) for row in rows]
