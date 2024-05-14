from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, UniqueConstraint, ForeignKey, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from app.models.utils_bd import virify_date
from hashlib import sha256
from datetime import datetime

Base = declarative_base()

#ESTA COMO DEVE SER
class Person(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(BLOB(256), nullable=False)  
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    cep = Column(String(9))
    cpf = Column(String(14), unique=True)
    rg = Column(String(20), unique=True)
    birth_date = Column(Date)
    sex = Column(Enum('Masculino', 'Feminino', 'Prefiro Não Declarar'))  
    civil_status = Column(Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'Outro'))
    profession = Column(String(100))
    salary = Column(DECIMAL(10, 2))  
    schooling = Column(Enum('Fundamental', 'Médio', 'Superior', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Outro'))
    language = Column(String(100))
    skills = Column(Text)  
    experience = Column(Text)  
    objective = Column(Text)  
    photo = Column(String(255))  # Sugestão: armazenar o caminho para a foto, não a foto em si
    cv = Column(String(255))  # Sugestão: armazenar o caminho para o currículo, não o currículo em si
    create_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('cpf','rg', 'email', name='_cpf_rg_email_uc'),  # Garante que tanto CPF quanto email sejam únicos
    )    

    def __init__(self, name, password, email, phone, address, city, state, country, cep, cpf, rg, birth_date, sex, civil_status, profession, salary,
                  schooling, language, skills, experience, objective, photo, cv):
        self.name = name
        self.password = sha256(password.encode()).digest()
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.cep = cep
        self.cpf = cpf
        self.rg = rg
        self.birth_date = birth_date
        self.sex = sex
        self.civil_status = civil_status
        self.profession = profession
        self.salary = salary
        self.schooling = schooling
        self.language = language
        self.skills = skills
        self.experience = experience
        self.objective = objective
        self.photo = photo
        self.cv = cv
        self.create_at = datetime.now()
    
    def get_cpf(self):
        return self.cpf

#NÃO UTILIZADO POR ENQUANTO
#ESTA COMO DEVE SER
class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, token, person_cpf):
        self.token = token
        self.person_cpf = person_cpf

#_______________________ADICIONADO_POR_CONTA_DO_FRONT_____________________________

#===================================CHECKLIST=====================================
#ESTA COMO DEVE SER
class CheckList(Base):
    __tablename__ = 'checklist'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    task = Column(Text) 
    status_of_task = Column(Enum('Em Espera', 'Iniciado', 'Finalizado'))  
    create_at = Column(DateTime)
    init_at = Column(DateTime)
    finish_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, title, task, status_of_task, init_at, finish_at, person_cpf):
        self.title = title
        self.task = task
        self.status_of_task = status_of_task
        self.create_at = datetime.now()
        self.init_at = virify_date(data_menor=datetime.now(),data_maior=init_at,param="início")
        self.finish_at = virify_date(data_menor=init_at,data_maior=finish_at,param="finalização")
        self.person_cpf = person_cpf

#==================================FEEDBACK=======================================
#ESTA COMO DEVE SER
class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    rating = Column(Enum('0', '1', '2','3', '4','5'))  
    create_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, comment, rating, person_cpf):
        self.comment = comment
        self.rating = rating
        self.create_at = datetime.now()
        self.person_cpf = person_cpf

#===============================QUESTIONS=AND=ANSWERS=============================
#ESTA COMO DEVE SER
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(Text) 
    create_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, question, person_cpf):
        self.question = question
        self.create_at = datetime.now()
        self.person_cpf = person_cpf

#ESTA COMO DEVE SER
class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    answer = Column(Text) 
    create_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)
    id_question = Column(Integer, ForeignKey('questions.id'), nullable=False)

    def __init__(self, answer, person_cpf, id_question):
        self.answer = answer
        self.create_at = datetime.now()
        self.person_cpf = person_cpf
        self.id_question = id_question

#=============================MEETING=AND=TRAINING===============================
#ESTA COMO DEVE SER
class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False) 
    create_at = Column(DateTime)
    init_at = Column(DateTime)
    finish_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, title, init_at, finish_at, person_cpf):
        self.title = title
        self.create_at = datetime.now()
        self.init_at = virify_date(data_menor=datetime.now(),data_maior=init_at,param="início")
        self.finish_at = virify_date(data_menor=init_at,data_maior=finish_at,param="finalização")
        self.person_cpf = person_cpf

#ESTA COMO DEVE SER
class Training(Base):
    __tablename__ = 'trainings'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    create_at = Column(DateTime)
    init_at = Column(DateTime)
    finish_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)

    def __init__(self, title, init_at, finish_at, person_cpf):
        self.title = title

        self.create_at = datetime.now()
        self.init_at = virify_date(data_menor=datetime.now(),data_maior=init_at,param="início")
        self.finish_at = virify_date(data_menor=init_at,data_maior=finish_at,param="finalização")
        self.person_cpf = person_cpf
#======================ADICIONADO=POR=CONTA=DO=FRONT======================================

engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
Base.metadata.create_all(engine)
