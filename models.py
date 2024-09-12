from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float,  String, UUID, Date
from database import Base
import uuid

class Admin(Base):
    __tablename__ ='admin'

    admin_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    admin_name=Column(String,index=True)
    admin_nic=Column(String,index=True)
    admin_phone=Column(String,index=True)
    admin_password=Column(String,index=True)
    admin_email=Column(String,index=True)

class Semester(Base):
    __tablename__ = 'semester'
    semester_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    year=Column(Integer,index=True)
    status=Column(Integer,index=True)
    semester=Column(Integer,index=True)

class Course(Base):
    __tablename__ = 'course'
    course_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    course_name=Column(String,index=True)
    enrollment_key=Column(String,index=True)
    course_description=Column(String,index=True)

class Program(Base):
    __tablename__ = 'program'
    program_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    duration=Column(String,index=True)
    program_name=Column(String,index=True)

class Affiliated_University(Base):
    __tablename__ = 'affiliated_university'
    affiliated_with=Column(String,index=True,primary_key=True)
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)

class Payment(Base):
    __tablename__ = 'payment'
    payment_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    date=Column(Date,index=True)
    type=Column(String,index=True)
    bank=Column(String,index=True)
    branch=Column(String,index=True)
    receipt_path=Column(String,index=True)
    amount=Column(Float,index=True)
    status=Column(String,index=True)
    student_number=Column(UUID, ForeignKey("student.student_id"),index = True)

class New_student(Base):
    __tablename__ = 'new_student'
    newStudent_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    name=Column(String,index=True)
    address=Column(String,index=True)
    gender=Column(String,index=True)
    email=Column(String,index=True)
    OL_path=Column(String,index=True)
    AL_path=Column(String)
    payment_id=Column(UUID, ForeignKey("payment.payment_id"),index=True)
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True)
    date=Column(Date,index=True)

class Student(Base):
    __tablename__ = 'student'
    student_id=Column(UUID,index=True,primary_key=True, default=uuid.uuid4)
    email=Column(String,index=True)
    password=Column(String,index=True)
    # newStudent_id=Column(UUID, ForeignKey("new_student.newStudent_id"),index=True)

class Course_semester_program(Base):
    __tablename__ = 'course_semester_program'
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
    semester_id=Column(UUID, ForeignKey("semester.semester_id"),index=True,primary_key=True)

#Lecturer models

class Lecturer(Base):
    __tablename__ = 'lecturer'
    lecturer_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    lecturer_name=Column(String,index=True)
    lecturer_nic=Column(String,index=True)
    lecturer_phone=Column(String,index=True)
    lecturer_email=Column(String,index=True)
    lecturer_password=Column(String,index=True)

class Lecturer_assigned_for (Base):
    __tablename__ = ' lecturer_assigned_for'
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
    semester_id=Column(UUID, ForeignKey("semester.semester_id"),index=True,primary_key=True)
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)
    lecturer_id=Column(UUID, ForeignKey("lecturer.lecturer_id"),index=True,primary_key=True)

class Section(Base):
    __tablename__ = 'section'
    section_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    section_name=Column(String,index=True)
    section_description=Column(String,index=True)
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True)

class Course_announcement(Base):
    __tablename__ = 'course_announcement'
    announcement_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    announcement_title=Column(String,index=True)
    announcement_description=Column(String,index=True)
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True)





