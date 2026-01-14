"""CLI 인터페이스"""
from carenote.models import Student, Consulting
from carenote.crud import StudentCRUD, ConsultingCRUD


def main_menu():
    """메인 메뉴"""
    while True:
        print("\n=== CareNote 개인상담기록 시스템 ===")
        print("1. 학생 관리")
        print("2. 상담 기록 관리")
        print("0. 종료")
        
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            student_menu()
        elif choice == '2':
            consulting_menu()
        elif choice == '0':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


def student_menu():
    """학생 관리 메뉴"""
    while True:
        print("\n--- 학생 관리 ---")
        print("1. 학생 등록")
        print("2. 학생 목록 조회")
        print("3. 학생 검색")
        print("4. 학생 정보 수정")
        print("5. 학생 삭제")
        print("0. 뒤로가기")
        
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            list_students()
        elif choice == '3':
            search_students()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '0':
            break
        else:
            print("잘못된 입력입니다.")


def add_student():
    """학생 등록"""
    print("\n=== 학생 등록 ===")
    name = input("이름: ").strip()
    phone = input("전화번호 (선택): ").strip() or None
    
    grade_input = input("학년 (1-6, 선택): ").strip()
    grade = int(grade_input) if grade_input else None
    
    class_input = input("반 (1-4, 선택): ").strip()
    class_num = int(class_input) if class_input else None
    
    sex = input("성별 (남/여, 선택): ").strip() or None
    
    student = Student(
        student_name=name,
        student_phone=phone,
        student_grade=grade,
        student_class=class_num,
        student_sex=sex
    )
    
    student_id = StudentCRUD.create(student)
    print(f"✓ 학생 등록 완료 (ID: {student_id})")


def list_students():
    """학생 목록 조회"""
    students = StudentCRUD.get_all()
    
    if not students:
        print("\n등록된 학생이 없습니다.")
        return
    
    print("\n=== 학생 목록 ===")
    print(f"{'ID':<5} {'이름':<10} {'학년':<5} {'반':<5} {'성별':<5} {'전화번호':<15}")
    print("-" * 60)
    
    for s in students:
        print(f"{s.student_id:<5} {s.student_name:<10} "
              f"{s.student_grade or '-':<5} {s.student_class or '-':<5} "
              f"{s.student_sex or '-':<5} {s.student_phone or '-':<15}")


def search_students():
    """학생 검색"""
    print("\n=== 학생 검색 ===")
    name = input("이름 (선택): ").strip() or None
    
    grade_input = input("학년 (선택): ").strip()
    grade = int(grade_input) if grade_input else None
    
    class_input = input("반 (선택): ").strip()
    class_num = int(class_input) if class_input else None
    
    students = StudentCRUD.search(name=name, grade=grade, class_num=class_num)
    
    if not students:
        print("\n검색 결과가 없습니다.")
        return
    
    print(f"\n검색 결과: {len(students)}명")
    print(f"{'ID':<5} {'이름':<10} {'학년':<5} {'반':<5} {'성별':<5}")
    print("-" * 40)
    
    for s in students:
        print(f"{s.student_id:<5} {s.student_name:<10} "
              f"{s.student_grade or '-':<5} {s.student_class or '-':<5} "
              f"{s.student_sex or '-':<5}")


def update_student():
    """학생 정보 수정"""
    student_id = int(input("\n수정할 학생 ID: ").strip())
    student = StudentCRUD.get(student_id)
    
    if not student:
        print("학생을 찾을 수 없습니다.")
        return
    
    print(f"\n현재 정보: {student.student_name} ({student.student_grade or '-'}학년 {student.student_class or '-'}반)")
    print("변경하지 않으려면 엔터를 누르세요.")
    
    updates = {}
    
    name = input(f"이름 [{student.student_name}]: ").strip()
    if name:
        updates['student_name'] = name
    
    grade = input(f"학년 [{student.student_grade or '-'}]: ").strip()
    if grade:
        updates['student_grade'] = int(grade)
    
    class_num = input(f"반 [{student.student_class or '-'}]: ").strip()
    if class_num:
        updates['student_class'] = int(class_num)
    
    if updates:
        StudentCRUD.update(student_id, **updates)
        print("✓ 학생 정보 수정 완료")
    else:
        print("변경사항이 없습니다.")


def delete_student():
    """학생 삭제"""
    student_id = int(input("\n삭제할 학생 ID: ").strip())
    student = StudentCRUD.get(student_id)
    
    if not student:
        print("학생을 찾을 수 없습니다.")
        return
    
    confirm = input(f"'{student.student_name}' 학생을 삭제하시겠습니까? (y/n): ").strip().lower()
    
    if confirm == 'y':
        StudentCRUD.delete(student_id)
        print("✓ 학생 삭제 완료 (관련 상담 기록도 삭제됨)")
    else:
        print("취소되었습니다.")


def consulting_menu():
    """상담 기록 관리 메뉴"""
    while True:
        print("\n--- 상담 기록 관리 ---")
        print("1. 상담 기록 추가")
        print("2. 상담 기록 조회 (학생별)")
        print("3. 전체 상담 기록 조회")
        print("4. 상담 기록 검색")
        print("5. 상담 기록 수정")
        print("6. 상담 기록 삭제")
        print("0. 뒤로가기")
        
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            add_consulting()
        elif choice == '2':
            view_consulting_by_student()
        elif choice == '3':
            list_all_consultings()
        elif choice == '4':
            search_consultings()
        elif choice == '5':
            update_consulting()
        elif choice == '6':
            delete_consulting()
        elif choice == '0':
            break
        else:
            print("잘못된 입력입니다.")


def add_consulting():
    """상담 기록 추가"""
    print("\n=== 상담 기록 추가 ===")
    
    student_id = int(input("학생 ID: ").strip())
    student = StudentCRUD.get(student_id)
    
    if not student:
        print("학생을 찾을 수 없습니다.")
        return
    
    print(f"학생: {student.student_name}")
    
    title = input("상담 주제: ").strip()
    consulting_type = input("상담 유형 (전화/대면/기타): ").strip() or None
    consulting_object = input("상담 대상 (본인/가족/교사/기타): ").strip() or None
    content = input("내담자가 진술한 문제와 상황: ").strip() or None
    opinion = input("상담자 소견 및 개입: ").strip() or None
    note = input("기타 특이사항: ").strip() or None
    
    consulting = Consulting(
        consulting_title=title,
        student_id=student_id,
        consulting_type=consulting_type,
        consulting_object=consulting_object,
        consulting_content=content,
        consulting_opinion=opinion,
        consulting_note=note
    )
    
    consulting_id = ConsultingCRUD.create(consulting)
    print(f"✓ 상담 기록 추가 완료 (ID: {consulting_id})")


def view_consulting_by_student():
    """학생별 상담 기록 조회"""
    student_id = int(input("\n학생 ID: ").strip())
    student = StudentCRUD.get(student_id)
    
    if not student:
        print("학생을 찾을 수 없습니다.")
        return
    
    consultings = ConsultingCRUD.get_by_student(student_id)
    
    if not consultings:
        print(f"\n{student.student_name} 학생의 상담 기록이 없습니다.")
        return
    
    print(f"\n=== {student.student_name} 학생 상담 기록 ({len(consultings)}건) ===")
    
    for c in consultings:
        print(f"\n[ID: {c.consulting_id}] {c.consulting_title}")
        print(f"일시: {c.consulting_date}")
        print(f"유형: {c.consulting_type or '-'} | 대상: {c.consulting_object or '-'}")
        if c.consulting_content:
            print(f"내용: {c.consulting_content[:50]}...")
        print("-" * 60)


def list_all_consultings():
    """전체 상담 기록 조회"""
    consultings = ConsultingCRUD.get_all()
    
    if not consultings:
        print("\n등록된 상담 기록이 없습니다.")
        return
    
    print(f"\n=== 전체 상담 기록 ({len(consultings)}건) ===")
    
    for c in consultings:
        student = StudentCRUD.get(c.student_id)
        print(f"\n[ID: {c.consulting_id}] {c.consulting_title}")
        print(f"학생: {student.student_name if student else '알 수 없음'}")
        print(f"일시: {c.consulting_date}")
        print(f"유형: {c.consulting_type or '-'}")
        print("-" * 60)


def search_consultings():
    """상담 기록 검색"""
    print("\n=== 상담 기록 검색 ===")
    title = input("주제 (선택): ").strip() or None
    student_name = input("학생 이름 (선택): ").strip() or None
    consulting_type = input("상담 유형 (선택): ").strip() or None
    
    consultings = ConsultingCRUD.search(
        title=title, 
        student_name=student_name, 
        consulting_type=consulting_type
    )
    
    if not consultings:
        print("\n검색 결과가 없습니다.")
        return
    
    print(f"\n검색 결과: {len(consultings)}건")
    
    for c in consultings:
        student = StudentCRUD.get(c.student_id)
        print(f"\n[ID: {c.consulting_id}] {c.consulting_title}")
        print(f"학생: {student.student_name if student else '알 수 없음'}")
        print(f"일시: {c.consulting_date}")
        print("-" * 60)


def update_consulting():
    """상담 기록 수정"""
    consulting_id = int(input("\n수정할 상담 기록 ID: ").strip())
    consulting = ConsultingCRUD.get(consulting_id)
    
    if not consulting:
        print("상담 기록을 찾을 수 없습니다.")
        return
    
    print(f"\n현재 정보: {consulting.consulting_title}")
    print("변경하지 않으려면 엔터를 누르세요.")
    
    updates = {}
    
    title = input(f"주제 [{consulting.consulting_title}]: ").strip()
    if title:
        updates['consulting_title'] = title
    
    content = input(f"내용 수정 (y/n): ").strip().lower()
    if content == 'y':
        updates['consulting_content'] = input("새 내용: ").strip()
    
    opinion = input(f"소견 수정 (y/n): ").strip().lower()
    if opinion == 'y':
        updates['consulting_opinion'] = input("새 소견: ").strip()
    
    if updates:
        ConsultingCRUD.update(consulting_id, **updates)
        print("✓ 상담 기록 수정 완료")
    else:
        print("변경사항이 없습니다.")


def delete_consulting():
    """상담 기록 삭제"""
    consulting_id = int(input("\n삭제할 상담 기록 ID: ").strip())
    consulting = ConsultingCRUD.get(consulting_id)
    
    if not consulting:
        print("상담 기록을 찾을 수 없습니다.")
        return
    
    confirm = input(f"'{consulting.consulting_title}' 기록을 삭제하시겠습니까? (y/n): ").strip().lower()
    
    if confirm == 'y':
        ConsultingCRUD.delete(consulting_id)
        print("✓ 상담 기록 삭제 완료")
    else:
        print("취소되었습니다.")
