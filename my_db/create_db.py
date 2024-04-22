from sqlalchemy import (create_engine, Integer, String, ForeignKey, DateTime)
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship

# docker run --name postgress -p 5432:5432 -e POSTGRES_PASSWORD=1111 -d postgres
# engine = create_engine('sqlite:///example.db', echo=False)  
# engine = create_engine('postgresql://user:password@localhost/mydatabase')  

engine = create_engine('postgresql://postgres:1111@localhost/postgres') 
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'))
    groups: Mapped['Group'] = relationship("Group")

class Teachers(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)

class TeachersSubject(Base):
    __tablename__ = "teaching_subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    teachers_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'))
    teachers: Mapped["Teachers"] = relationship("Teachers")

class Jornal(Base):
    __tablename__ = "journal"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    students: Mapped['Student'] = relationship("Student")
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('teaching_subjects.id'))
    subject: Mapped['TeachersSubject'] = relationship("TeachersSubject")
    rating: Mapped[int] = mapped_column(Integer)
    date_of_rating: Mapped[int] = mapped_column(DateTime)

#Base.metadata.create_all(engine)
