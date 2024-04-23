from sqlalchemy import func
from my_db.create_db import Group, Student, Teachers, TeachersSubject, Jornal 
from my_db.create_db import session


def request_1():
    """5 students with the highest average score in all subjects"""
    query = session.query(
        Student.id.label('student_id'),
        Student.first_name,
        Student.last_name,
        func.avg(Jornal.rating).label('average_grade')
        ).join(Jornal, Student.id == Jornal.student_id).group_by(Student.id).order_by(func.avg(Jornal.rating).desc()).limit(5)

    results = query.all()

    for result in results:
        print(f"Student ID: {result.student_id:^4}| Name: {result.first_name:<10} {result.last_name:<15}| Rating: {result.average_grade}")

def request_2(ts_id:int = 1):
    """The student with the highest average score in a certain subject"""
    query = session.query(
        Student.id.label('student_id'),
        Student.first_name,
        Student.last_name,
        func.avg(Jornal.rating).label('average_grade')
        ).join(Jornal, Student.id == Jornal.student_id)\
        .join(TeachersSubject, Jornal.subject_id == TeachersSubject.id)\
        .filter(TeachersSubject.id == ts_id)\
        .group_by(Student.id)\
        .order_by(func.avg(Jornal.rating).desc())\
        .limit(1)

    result = query.first()
    print(f"Student ID: {result.student_id:^4}| Name: {result.first_name:<10} {result.last_name:<15}| Rating: {result.average_grade}")

def request_3(ts_id:int = 1):
    """The average score in groups for a certain subject"""
    query = session.query(
        Group.group_name,
        func.avg(Jornal.rating).label('average_grade')
        ).join(Student, Group.id == Student.group_id)\
        .join(Jornal, Student.id == Jornal.student_id)\
        .join(TeachersSubject, Jornal.subject_id == TeachersSubject.id)\
        .filter(TeachersSubject.id == ts_id)\
        .group_by(Group.group_name)\
        .order_by(Group.group_name)

    results = query.all()
    for result in results:
        print(f"{result.group_name:<35}| Rating: {result.average_grade}")

def request_4():
    """grade point average"""
    query = session.query(func.avg(Jornal.rating).label('average_grade'))
    result = query.first()
    print(result.average_grade)

def request_5(t_id:int = 1):
    """Courses taught by a teacher"""
    query = session.query(TeachersSubject.subject_name)\
               .join(Teachers, TeachersSubject.teachers_id == Teachers.id)\
               .filter(Teachers.id == t_id)

    results = query.all()

    for result in results:
        print(f"Subject name: {result.subject_name}")

def request_6(g_id:int = 1):
    """List of students in a particular group"""
    query = session.query(Student)\
               .filter(Student.group_id == g_id)\
               .with_entities(Student.id, Student.first_name, Student.last_name, Student.group_id)

    results = query.all()

    for result in results:
        print(f"Student ID: {result.id:<3}| Name: {result.first_name:<10} {result.last_name:<15} | Group ID: {result.group_id:<5}")

def request_7(g_id:int = 1, ts_id:int = 1):
    """Evaluations of students in a separate group on a certain subject."""
    query = session.query(
        Student.first_name,
        Student.last_name,
        TeachersSubject.subject_name,
        Jornal.rating,
        Jornal.date_of_rating,
        Group.group_name
        ).join(Group, Student.group_id == Group.id)\
        .join(Jornal, Student.id == Jornal.student_id)\
        .join(TeachersSubject, Jornal.subject_id == TeachersSubject.id)\
        .filter(Group.id == g_id, TeachersSubject.id == ts_id)

    results = query.all()

    for result in results:
        print(f"Name: {result.first_name:<10} {result.last_name:<15} | {result.subject_name:^20} | Rating: {result.rating:^4} | {result.date_of_rating} | {result.group_name:^20}")

def request_8(t_id:int = 1):
    """The average score given by a certain teacher in his subjects"""
    query = session.query(
        Teachers.first_name,
        Teachers.last_name,
        func.avg(Jornal.rating).label('average_rating')
        ).join(TeachersSubject, TeachersSubject.teachers_id == Teachers.id)\
        .join(Jornal, Jornal.subject_id == TeachersSubject.id)\
        .filter(Teachers.id == t_id)\
        .group_by(Teachers.first_name, Teachers.last_name)

    results = query.all()

    for result in results:
        print(f"Name: {result.first_name:<10}{result.last_name:<15}| Rating: {result.average_rating}")

def request_9(s_id:int = 1):
    """List of courses attended by a particular student"""
    query = session.query(TeachersSubject.subject_name)\
               .join(Jornal, Jornal.subject_id == TeachersSubject.id)\
               .filter(Jornal.student_id == s_id)\
               .distinct()

    results = query.all()

    for result in results:
        print(result.subject_name)

def request_10(s_id:int = 1, t_id:int = 1):
    """List of courses taught to a specific student by a specific teacher"""
    query = session.query(
        TeachersSubject.subject_name,
        Teachers.first_name,
        Teachers.last_name,
        Jornal.student_id
        ).join(Teachers, TeachersSubject.teachers_id == Teachers.id)\
        .join(Jornal, Jornal.subject_id == TeachersSubject.id)\
        .filter(Jornal.student_id == s_id, Teachers.id == t_id)\
        .distinct()

    results = query.all()

    for result in results:
        print(f"{result.subject_name:<20}| Name: {result.first_name:<10} {result.last_name:<15}| Student ID:{result.student_id:^3}")


if __name__=="__main__":
    request_10()