"""데이터 모델"""
import json
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class Student:
    """학생 모델"""
    student_name: str
    student_id: Optional[int] = None
    student_phone: Optional[str] = None
    student_grade: Optional[int] = None
    student_class: Optional[int] = None
    student_sex: Optional[str] = None
    student_history: str = '[]'
    
    def get_history(self) -> List[Dict]:
        """히스토리를 리스트로 반환"""
        return json.loads(self.student_history)
    
    def add_history(self, grade: int, class_num: int):
        """히스토리에 새 항목 추가"""
        history = self.get_history()
        history.append({"grade": grade, "class": class_num})
        self.student_history = json.dumps(history, ensure_ascii=False)
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Consulting:
    """상담 모델"""
    consulting_title: str
    student_id: int
    consulting_id: Optional[int] = None
    consulting_date: Optional[str] = None
    consulting_type: Optional[str] = None
    consulting_object: Optional[str] = None
    consulting_content: Optional[str] = None
    consulting_opinion: Optional[str] = None
    consulting_note: Optional[str] = None
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {k: v for k, v in asdict(self).items() if v is not None}
