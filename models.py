from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float,  String, UUID, Date,func
from database import Base
import uuid
import datetime

class Admin(Base):
    __tablename__ ='admin'

    admin_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    admin_name=Column(String,index=True)
    admin_nic=Column(String,index=True)
    admin_phone=Column(String,index=True)
    admin_password=Column(String,index=True)
    admin_email=Column(String,index=True)
    image_path=Column(String,index=True)

class AdminAnnouncement(Base):
    __tablename__ ='admin_announcement'

    announcement_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title=Column(String,index=True)
    description=Column(String,index=True)
    admin_id=Column(UUID, ForeignKey("admin.admin_id"),index=True)

class Semester(Base): 
    __tablename__ = 'semester'
    semester_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    year=Column(Integer,index=True)
    status=Column(Integer,index=True)
    semester=Column(Integer,index=True)
    # program_id=Column(UUID, ForeignKey("program.program_id"),index=True) ##Changed

class Course(Base):
    __tablename__ = 'course'
    course_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    course_name=Column(String,index=True)
    enrollment_key=Column(String,index=True)
    course_description=Column(String,index=True)
    course_image=Column(String,index=True, default=None)
    # semester_id=Column(UUID, ForeignKey("semester.semester_id"),index=True) ##Changed

class Program(Base):
    __tablename__ = 'program'
    program_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    duration=Column(String,index=True)
    program_name=Column(String,index=True)
    program_description=Column(String,index=True)
    university_name=Column(String,index=True)
    university_image=Column(String,index=True)

class Affiliated_University(Base):
    __tablename__ = 'affiliated_university'
    affiliated_with=Column(String,index=True,primary_key=True)
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)

class Payment(Base):
    __tablename__ = 'payment'
    payment_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    date=Column(Date, default=datetime.date.today, index=True)
    receipt_path=Column(String,index=True)
    student_id=Column(UUID, ForeignKey("student.student_id"),index = True)
    confirmed=Column(Boolean,index=True,default=False)

class New_student(Base):
    __tablename__ = 'new_student'
    newStudent_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    name=Column(String,index=True)
    address=Column(String,index=True)
    email=Column(String,index=True)
    OL_path=Column(String,index=True)
    AL_path=Column(String)
    payment_path=Column(String,index=True)
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True)
    date = Column(Date, default=datetime.date.today, index=True)
    confirmed = Column(Boolean,index=True,default=False)

class Student(Base):
    __tablename__ = 'student'
    student_id=Column(UUID,index=True,primary_key=True, default=uuid.uuid4)
    email=Column(String,index=True)
    password=Column(String,index=True)
    semester_id=Column(UUID,ForeignKey("semester.semester_id"), index=True)
    newStudent_id=Column(UUID, ForeignKey("new_student.newStudent_id"),index=True)
    image_path=Column(String,index=True, default=None)

class Student_enrolled_course(Base):
    __tablename__ = 'student_enrolled_courses'
    course_id=Column(UUID,ForeignKey("course.course_id"),index=True,primary_key=True,)
    student_id=Column(UUID,ForeignKey("student.student_id"),index=True,primary_key=True,)
    semester_id=Column(UUID,ForeignKey("semester.semester_id"), primary_key=True, index=True )


class Course_semester_program(Base):
    __tablename__ = 'course_semester_program'
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
    semester_id=Column(UUID, ForeignKey("semester.semester_id"),index=True,primary_key=True)

class Program_semester_student(Base):
    __tablename__ = 'program_semester_student'
    program_id=Column(UUID, ForeignKey("program.program_id"),index=True,primary_key=True)
    semester_id=Column(UUID, ForeignKey("semester.semester_id"),index=True,primary_key=True)
    student_id=Column(UUID, ForeignKey("student.student_id"),index=True,primary_key=True)

#Lecturer models

class Lecturer(Base):
    __tablename__ = 'lecturer'
    lecturer_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    lecturer_name=Column(String,index=True)
    lecturer_nic=Column(String,index=True)
    lecturer_phone=Column(String,index=True)
    lecturer_email=Column(String,index=True)
    lecturer_password=Column(String,index=True)
    lecturer_image=Column(String,index=True, default=None)

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
    course_id=Column(UUID, ForeignKey("course.course_id", ondelete="CASCADE"),index=True)

class Course_announcement(Base):
    __tablename__ = 'course_announcement'
    announcement_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    announcement_title=Column(String,index=True)
    announcement_description=Column(String,index=True)
    course_id=Column(UUID, ForeignKey("course.course_id", ondelete="CASCADE"),index=True)

class Course_material(Base):
    __tablename__ = 'course_material'
    material_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    material_name=Column(String,index=True)
    material_path=Column(String,index=True)
    section_id=Column(UUID, ForeignKey("section.section_id", ondelete="CASCADE"),index=True)

class Quiz(Base):
    __tablename__ = 'quiz'
    quiz_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    quiz_name=Column(String,index=True)
    quiz_duration=Column(Integer,index=True)
    quiz_total_marks=Column(Integer,index=True)
    quiz_description=Column(String,index=True)
    quiz_password=Column(String,index=True)
    quiz_no_of_questions=Column(Integer,index=True)
    section_id=Column(UUID, ForeignKey("section.section_id", ondelete="CASCADE"),index=True)
    is_enabled = Column(Boolean,index=True,default=True)
    attempts= Column(Integer,index=True,default = 1)

class Question(Base):
    __tablename__ = 'question'
    question_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    question=Column(String,index=True)
    marks=Column(Integer,index=True)
    question_type=Column(String,index=True)
    quiz_id=Column(UUID, ForeignKey("quiz.quiz_id", ondelete="CASCADE"),index=True)

class Answer(Base):
    __tablename__ = 'answer'
    answer_id=Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    answer=Column(String,index=True)
    is_correct=Column(Boolean,index=True)
    question_id=Column(UUID, ForeignKey("question.question_id", ondelete="CASCADE"),index=True)

class StudentAttempts(Base):
    __tablename__ = 'student_attempt'
    id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid.uuid4)
    quiz_id=Column(UUID, ForeignKey("quiz.quiz_id"),index=True)
    course_id=Column(UUID, ForeignKey("course.course_id"),index=True)
    is_doing = Column(Boolean,index=True,default=True)
    student_id =Column(UUID, ForeignKey("student.student_id"),index=True)
    mcq_marks = Column(Integer,index=True,default=0)
    written_marks = Column(Integer,index=True,default=0)

class StudentWrittenAnswers(Base):
    __tablename__ = 'student_written_answer'
    student_id = Column(UUID,ForeignKey("student.student_id"),index=True,primary_key=True)
    quiz_id=Column(UUID, ForeignKey("quiz.quiz_id"),index=True,primary_key=True)
    course_id= Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
    marks = Column(Integer,index=True,default=0)
    question_id =Column(UUID,ForeignKey("question.question_id"),index=True,primary_key=True)
    answer= Column(String,index=True)

class StudentMCQAnswers(Base):
    __tablename__ = 'student_mcq_answer'
    id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid.uuid4)
    student_id = Column(UUID,ForeignKey("student.student_id"),index=True)
    quiz_id=Column(UUID, ForeignKey("quiz.quiz_id"),index=True)
    course_id= Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
    question_id =Column(UUID,ForeignKey("question.question_id"),index=True)
    answer_id= Column(UUID,ForeignKey("answer.answer_id"),index=True)
    marks = Column(Integer,index=True,default=0)

# class StudentWrittenAnswers(Base):
#     __tablename__ = 'student_written_answer'
#     student_id = Column(UUID,ForeignKey("student.student_id"),index=True,primary_key=True)
#     quiz_id=Column(UUID, ForeignKey("quiz.quiz_id"),index=True,primary_key=True)
#     course_id= Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
#     marks = Column(Integer,index=True)
#     question_id =Column(UUID,ForeignKey("question.question_id"),index=True,primary_key=True)
#     answer= Column(String,index=True)
#     marks = Column(Integer,index=True,default=0)

# class StudentMCQAnswers(Base):
#     __tablename__ = 'student_mcq_answer'
#     id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid.uuid4)
#     student_id = Column(UUID,ForeignKey("student.student_id"),index=True)
#     quiz_id=Column(UUID, ForeignKey("quiz.quiz_id"),index=True)
#     course_id= Column(UUID, ForeignKey("course.course_id"),index=True,primary_key=True)
#     question_id =Column(UUID,ForeignKey("question.question_id"),index=True)
#     answer_id= Column(UUID,ForeignKey("answer.answer_id"),index=True)
#     marks = Column(Integer,index=True,default=0)