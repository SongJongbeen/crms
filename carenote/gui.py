from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox,
    QListWidget, QFormLayout, QSpinBox, QTableWidget, QTableWidgetItem,
    QSplitter, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
import sys

from carenote.crud import StudentCRUD, ConsultingCRUD
from carenote.models import Student, Consulting
from carenote.database import init_database

class StudentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ----- 상단: 학생 검색 / 리스트 -----
        search_layout = QHBoxLayout()
        self.search_name_input = QLineEdit()
        self.search_name_input.setPlaceholderText("이름으로 검색")
        self.search_btn = QPushButton("검색")
        self.search_btn.clicked.connect(self.search_students)

        search_layout.addWidget(self.search_name_input)
        search_layout.addWidget(self.search_btn)

        self.student_list = QListWidget()
        self.student_list.itemSelectionChanged.connect(self.on_student_selected)

        layout.addLayout(search_layout)
        layout.addWidget(self.student_list)

        # ----- 하단: 학생 상세 입력 폼 -----
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow("이름*", self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("예: 010-1234-5678")
        form_layout.addRow("전화번호", self.phone_input)

        # 학년: 1~6 드롭다운
        self.grade_combo = QComboBox()
        self.grade_combo.addItem("선택 안 함", None)
        for g in range(1, 7):
            self.grade_combo.addItem(f"{g}학년", g)
        form_layout.addRow("학년", self.grade_combo)

        # 반: 1~4 드롭다운
        self.class_combo = QComboBox()
        self.class_combo.addItem("선택 안 함", None)
        for c in range(1, 5):
            self.class_combo.addItem(f"{c}반", c)
        form_layout.addRow("반", self.class_combo)

        # 성별: 드롭다운
        self.sex_combo = QComboBox()
        self.sex_combo.addItem("선택 안 함", None)
        self.sex_combo.addItem("남", "남")
        self.sex_combo.addItem("여", "여")
        form_layout.addRow("성별", self.sex_combo)

        layout.addLayout(form_layout)

        # 버튼들
        btn_layout = QHBoxLayout()
        self.new_btn = QPushButton("새 학생")
        self.save_btn = QPushButton("저장/업데이트")
        self.delete_btn = QPushButton("삭제")

        self.new_btn.clicked.connect(self.clear_form)
        self.save_btn.clicked.connect(self.save_student)
        self.delete_btn.clicked.connect(self.delete_student)

        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 현재 선택된 student_id
        self.current_student_id = None
        self.load_all_students()

    # ---------- 유틸 / 검증 ----------

    def show_error(self, message: str):
        QMessageBox.critical(self, "입력 오류", message)

    def validate_student_form(self) -> bool:
        name = self.name_input.text().strip()
        if not name:
            self.show_error("이름은 필수입니다.")
            return False

        # phone은 형식 강제까지는 안 하고, 나중에 정규식 넣어도 됨
        # grade / class / sex는 드롭다운 값이기 때문에 이미 검증됨
        return True

    def get_selected_grade(self):
        data = self.grade_combo.currentData()
        return int(data) if data is not None else None

    def get_selected_class(self):
        data = self.class_combo.currentData()
        return int(data) if data is not None else None

    def get_selected_sex(self):
        return self.sex_combo.currentData()

    # ---------- CRUD 동작 ----------

    def load_all_students(self):
        self.student_list.clear()
        students = StudentCRUD.get_all()
        for s in students:
            self.student_list.addItem(f"{s.student_id}: {s.student_name}")

    def search_students(self):
        keyword = self.search_name_input.text().strip() or None
        students = StudentCRUD.search(name=keyword)
        self.student_list.clear()
        for s in students:
            self.student_list.addItem(f"{s.student_id}: {s.student_name}")

    def on_student_selected(self):
        items = self.student_list.selectedItems()
        if not items:
            return
        text = items[0].text()  # "id: name"
        student_id = int(text.split(":")[0])
        student = StudentCRUD.get(student_id)
        if not student:
            return

        self.current_student_id = student.student_id
        self.name_input.setText(student.student_name)
        self.phone_input.setText(student.student_phone or "")

        # 콤보박스 값 설정
        # grade
        if student.student_grade:
            index = self.grade_combo.findData(student.student_grade)
            if index != -1:
                self.grade_combo.setCurrentIndex(index)
        else:
            self.grade_combo.setCurrentIndex(0)

        # class
        if student.student_class:
            index = self.class_combo.findData(student.student_class)
            if index != -1:
                self.class_combo.setCurrentIndex(index)
        else:
            self.class_combo.setCurrentIndex(0)

        # sex
        if student.student_sex:
            index = self.sex_combo.findData(student.student_sex)
            if index != -1:
                self.sex_combo.setCurrentIndex(index)
        else:
            self.sex_combo.setCurrentIndex(0)

    def clear_form(self):
        self.current_student_id = None
        self.name_input.clear()
        self.phone_input.clear()
        self.grade_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.sex_combo.setCurrentIndex(0)
        self.student_list.clearSelection()

    def save_student(self):
        if not self.validate_student_form():
            return  # 검증 실패 → NEXT(저장) 막기

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip() or None
        grade = self.get_selected_grade()
        class_num = self.get_selected_class()
        sex = self.get_selected_sex()

        if self.current_student_id is None:
            # 신규 생성
            student = Student(
                student_name=name,
                student_phone=phone,
                student_grade=grade,
                student_class=class_num,
                student_sex=sex,
            )
            new_id = StudentCRUD.create(student)
            QMessageBox.information(self, "완료", f"학생이 추가되었습니다. (ID: {new_id})")
        else:
            # 업데이트
            updates = {
                "student_name": name,
                "student_phone": phone,
                "student_grade": grade,
                "student_class": class_num,
                "student_sex": sex,
            }
            StudentCRUD.update(self.current_student_id, **updates)
            QMessageBox.information(self, "완료", "학생 정보가 수정되었습니다.")

        self.load_all_students()

    def delete_student(self):
        if self.current_student_id is None:
            self.show_error("삭제할 학생을 선택하세요.")
            return

        reply = QMessageBox.question(
            self,
            "확인",
            "학생과 관련 상담 기록이 모두 삭제됩니다. 계속하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            StudentCRUD.delete(self.current_student_id)
            self.clear_form()
            self.load_all_students()

class ConsultingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_student_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ----- 학생 선택 영역 (이름 검색 -> 목록 선택) -----
        student_layout = QHBoxLayout()
        self.student_search_input = QLineEdit()
        self.student_search_input.setPlaceholderText("학생 이름 검색")
        self.student_search_btn = QPushButton("검색")
        self.student_search_btn.clicked.connect(self.search_students)

        self.student_search_list = QListWidget()
        self.student_search_list.itemSelectionChanged.connect(
            self.on_student_selected
        )

        student_layout.addWidget(self.student_search_input)
        student_layout.addWidget(self.student_search_btn)

        layout.addLayout(student_layout)
        layout.addWidget(QLabel("검색 결과에서 학생을 선택하세요"))
        layout.addWidget(self.student_search_list)

        # ----- 상담 입력 폼 -----
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        form_layout.addRow("상담 주제*", self.title_input)

        # 상담 유형 드롭다운
        self.type_combo = QComboBox()
        self.type_combo.addItem("선택 안 함", None)
        for t in ["전화", "대면", "기타"]:
            self.type_combo.addItem(t, t)
        form_layout.addRow("상담 유형", self.type_combo)

        # 상담 대상 드롭다운
        self.object_combo = QComboBox()
        self.object_combo.addItem("선택 안 함", None)
        for o in ["본인", "가족", "교사", "기타"]:
            self.object_combo.addItem(o, o)
        form_layout.addRow("상담 대상", self.object_combo)

        self.content_edit = QTextEdit()
        form_layout.addRow("진술 내용", self.content_edit)

        self.opinion_edit = QTextEdit()
        form_layout.addRow("소견 및 개입", self.opinion_edit)

        self.note_edit = QTextEdit()
        form_layout.addRow("기타 특이사항", self.note_edit)

        layout.addLayout(form_layout)

        # ----- 버튼 영역 -----
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("상담 기록 추가")
        self.save_btn.clicked.connect(self.save_consulting)

        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    # ---------- 유틸 / 검증 ----------

    def show_error(self, msg: str):
        QMessageBox.critical(self, "입력 오류", msg)

    def validate_form(self) -> bool:
        if self.selected_student_id is None:
            self.show_error("학생을 먼저 검색하고 선택해야 합니다.")
            return False

        title = self.title_input.text().strip()
        if not title:
            self.show_error("상담 주제는 필수입니다.")
            return False

        # 드롭다운 값은 이미 제한되어 있으므로 별도 체크 필요 없음
        return True

    def get_selected_type(self):
        return self.type_combo.currentData()

    def get_selected_object(self):
        return self.object_combo.currentData()

    # ---------- 동작 ----------

    def search_students(self):
        keyword = self.student_search_input.text().strip() or None
        students = StudentCRUD.search(name=keyword)
        self.student_search_list.clear()
        for s in students:
            # "id: 이름 (학년/반)" 정도로 보여주기
            extra = ""
            if s.student_grade and s.student_class:
                extra = f" ({s.student_grade}학년 {s.student_class}반)"
            self.student_search_list.addItem(f"{s.student_id}: {s.student_name}{extra}")

    def on_student_selected(self):
        items = self.student_search_list.selectedItems()
        if not items:
            self.selected_student_id = None
            return
        text = items[0].text()
        student_id = int(text.split(":")[0])
        self.selected_student_id = student_id

    def save_consulting(self):
        if not self.validate_form():
            return  # 검증 실패 → NEXT(저장) 차단

        consulting = Consulting(
            consulting_title=self.title_input.text().strip(),
            student_id=self.selected_student_id,
            consulting_type=self.get_selected_type(),
            consulting_object=self.get_selected_object(),
            consulting_content=self.content_edit.toPlainText().strip() or None,
            consulting_opinion=self.opinion_edit.toPlainText().strip() or None,
            consulting_note=self.note_edit.toPlainText().strip() or None,
        )
        cid = ConsultingCRUD.create(consulting)
        QMessageBox.information(self, "완료", f"상담 기록이 추가되었습니다. (ID: {cid})")

        # 폼 초기화
        self.title_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.object_combo.setCurrentIndex(0)
        self.content_edit.clear()
        self.opinion_edit.clear()
        self.note_edit.clear()

class ConsultingListTab(QWidget):
    """상담 기록 조회/검색 탭"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ---- 검색 영역 ----
        search_layout = QHBoxLayout()

        self.search_name_input = QLineEdit()
        self.search_name_input.setPlaceholderText("학생 이름")

        self.search_title_input = QLineEdit()
        self.search_title_input.setPlaceholderText("상담 주제")

        self.search_type_combo = QComboBox()
        self.search_type_combo.addItem("상담 유형 전체", None)
        for t in ["전화", "대면", "기타"]:
            self.search_type_combo.addItem(t, t)

        # 날짜 범위: QDateEdit + 달력 팝업
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)  # 작은 달력 팝업 [web:55][web:63]
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))  # 기본: 한 달 전

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_date_edit.setDate(QDate.currentDate())  # 기본: 오늘

        self.search_btn = QPushButton("검색")
        self.search_btn.clicked.connect(self.search_consultings)

        search_layout.addWidget(self.search_name_input)
        search_layout.addWidget(self.search_title_input)
        search_layout.addWidget(self.search_type_combo)
        search_layout.addWidget(QLabel("시작일"))
        search_layout.addWidget(self.start_date_edit)
        search_layout.addWidget(QLabel("종료일"))
        search_layout.addWidget(self.end_date_edit)
        search_layout.addWidget(self.search_btn)

        main_layout.addLayout(search_layout)

        # ---- 목록 + 상세를 나누는 splitter ----
        splitter = QSplitter(Qt.Orientation.Vertical)

        # 상단: 상담 리스트 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "학생", "일시", "유형", "주제"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)

        splitter.addWidget(self.table)

        # 하단: 상세 내용
        detail_widget = QWidget()
        detail_layout = QFormLayout()

        self.detail_student_label = QLabel("-")
        self.detail_date_label = QLabel("-")
        self.detail_type_label = QLabel("-")
        self.detail_object_label = QLabel("-")
        self.detail_title_label = QLabel("-")

        self.detail_content_edit = QTextEdit()
        self.detail_content_edit.setReadOnly(True)
        self.detail_opinion_edit = QTextEdit()
        self.detail_opinion_edit.setReadOnly(True)
        self.detail_note_edit = QTextEdit()
        self.detail_note_edit.setReadOnly(True)

        detail_layout.addRow("학생", self.detail_student_label)
        detail_layout.addRow("일시", self.detail_date_label)
        detail_layout.addRow("유형", self.detail_type_label)
        detail_layout.addRow("대상", self.detail_object_label)
        detail_layout.addRow("주제", self.detail_title_label)
        detail_layout.addRow("진술 내용", self.detail_content_edit)
        detail_layout.addRow("소견 및 개입", self.detail_opinion_edit)
        detail_layout.addRow("기타 특이사항", self.detail_note_edit)

        detail_widget.setLayout(detail_layout)
        splitter.addWidget(detail_widget)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        # 처음 로딩 시 전체 보기
        self.load_all_consultings()

    # ---- 데이터 로딩/검색 ----

    def load_all_consultings(self):
        consultings = ConsultingCRUD.get_all()
        self.populate_table(consultings)

    def search_consultings(self):
        title = self.search_title_input.text().strip() or None
        student_name = self.search_name_input.text().strip() or None
        consulting_type = self.search_type_combo.currentData()

        # 날짜 범위 문자열로 (SQLite TEXT 비교용)
        start_qdate = self.start_date_edit.date()
        end_qdate = self.end_date_edit.date()

        start_date_str = start_qdate.toString("yyyy-MM-dd") + " 00:00:00"
        end_date_str = end_qdate.toString("yyyy-MM-dd") + " 23:59:59"

        # 종료일이 시작일보다 빠르면 막기
        if end_qdate < start_qdate:
            QMessageBox.critical(self, "입력 오류", "종료일은 시작일보다 빠를 수 없습니다.")
            return  # 잘못된 입력이므로 검색(NEXT) 막기

        consultings = ConsultingCRUD.search(
            title=title,
            student_name=student_name,
            consulting_type=consulting_type,
            start_date=start_date_str,
            end_date=end_date_str,
        )
        self.populate_table(consultings)

    def populate_table(self, consultings):
        self.table.clearContents()
        self.table.setRowCount(len(consultings))

        for row, c in enumerate(consultings):
            student = StudentCRUD.get(c.student_id)
            student_name = student.student_name if student else "알 수 없음"

            self.table.setItem(row, 0, QTableWidgetItem(str(c.consulting_id)))
            self.table.setItem(row, 1, QTableWidgetItem(student_name))
            self.table.setItem(row, 2, QTableWidgetItem(c.consulting_date or ""))
            self.table.setItem(row, 3, QTableWidgetItem(c.consulting_type or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(c.consulting_title or ""))

        self.table.resizeColumnsToContents()

        # 목록이 비었으면 상세 영역 초기화
        if not consultings:
            self.clear_detail()
        else:
            # 첫 행 자동 선택
            self.table.selectRow(0)

    # ---- 상세 표시 ----

    def clear_detail(self):
        self.detail_student_label.setText("-")
        self.detail_date_label.setText("-")
        self.detail_type_label.setText("-")
        self.detail_object_label.setText("-")
        self.detail_title_label.setText("-")
        self.detail_content_edit.clear()
        self.detail_opinion_edit.clear()
        self.detail_note_edit.clear()

    def on_row_selected(self):
        items = self.table.selectedItems()
        if not items:
            self.clear_detail()
            return

        row = items[0].row()
        consulting_id_item = self.table.item(row, 0)
        if not consulting_id_item:
            self.clear_detail()
            return

        consulting_id = int(consulting_id_item.text())
        consulting = ConsultingCRUD.get(consulting_id)
        if not consulting:
            self.clear_detail()
            return

        student = StudentCRUD.get(consulting.student_id)
        student_name = student.student_name if student else "알 수 없음"

        self.detail_student_label.setText(student_name)
        self.detail_date_label.setText(consulting.consulting_date or "-")
        self.detail_type_label.setText(consulting.consulting_type or "-")
        self.detail_object_label.setText(consulting.consulting_object or "-")
        self.detail_title_label.setText(consulting.consulting_title or "-")
        self.detail_content_edit.setPlainText(
            consulting.consulting_content or ""
        )
        self.detail_opinion_edit.setPlainText(
            consulting.consulting_opinion or ""
        )
        self.detail_note_edit.setPlainText(
            consulting.consulting_note or ""
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CareNote - 개인상담기록 통합시스템")

        tabs = QTabWidget()
        tabs.addTab(StudentTab(), "학생 관리")
        tabs.addTab(ConsultingTab(), "상담 기록")
        tabs.addTab(ConsultingListTab(), "상담 기록 조회")

        self.setCentralWidget(tabs)
        self.resize(1000, 650)


def apply_basic_style(app: QApplication):
    # 아주 간단한 다크 스타일
    app.setStyleSheet("""
        QMainWindow {
            background-color: #222;
        }
        QWidget {
            font-family: 'Malgun Gothic';
            font-size: 11pt;
            color: #f0f0f0;
        }
        QLineEdit, QTextEdit, QListWidget, QComboBox {
            background-color: #333;
            border: 1px solid #555;
            padding: 4px;
        }
        QPushButton {
            background-color: #3a7bd5;
            border: none;
            padding: 6px 10px;
            color: white;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #356ac3;
        }
        QPushButton:pressed {
            background-color: #2b579a;
        }
        QTabBar::tab {
            padding: 8px 16px;
        }
    """)
