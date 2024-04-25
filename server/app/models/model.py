from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, UniqueConstraint, ForeignKey, DateTime, BinaryExpression, BINARY, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from hashlib import sha256
from datetime import datetime

Base = declarative_base()

class Person(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(BLOB(256), nullable=False)  # Sugestão: usar uma função de hash para armazenar senhas de forma segura
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
    sex = Column(Enum('Masculino', 'Feminino', 'Prefiro Não Declarar'))  # Sugestão: usar ENUM para sexo
    civil_status = Column(Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'Outro'))
    profession = Column(String(100))
    salary = Column(DECIMAL(10, 2))  # Sugestão: usar DECIMAL para valores monetários
    schooling = Column(Enum('Fundamental', 'Médio', 'Superior', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Outro'))
    language = Column(String(100))
    skills = Column(Text)  # Sugestão: armazenar habilidades em um formato de texto ou JSON
    experience = Column(Text)  # Sugestão: armazenar experiência em um formato de texto ou JSON
    objective = Column(Text)  # Sugestão: armazenar objetivo em um formato de texto ou JSON
    photo = Column(String(255))  # Sugestão: armazenar o caminho para a foto, não a foto em si
    cv = Column(String(255))  # Sugestão: armazenar o caminho para o currículo, não o currículo em si
    create_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('cpf','rg', 'email', name='_cpf_rg_email_uc'),  # Garante que tanto CPF quanto email sejam únicos
    )    

    def __init__(self, nome, senha, email, telefone, endereco, cidade, estado, pais, cep, cpf, rg, data_nascimento, sexo, estado_civil, profissao, salario, escolaridade, idioma, habilidades, experiencia, objetivo, foto, curriculo):
        self.name = nome
        self.password = sha256(senha.encode()).digest()
        self.email = email
        self.phone = telefone
        self.address = endereco
        self.city = cidade
        self.state = estado
        self.country = pais
        self.cep = cep
        self.cpf = cpf
        self.rg = rg
        self.birth_date = data_nascimento
        self.sex = sexo
        self.civil_status = estado_civil
        self.profession = profissao
        self.salary = salario
        self.schooling = escolaridade
        self.language = idioma
        self.skills = habilidades
        self.experience = experiencia
        self.objective = objetivo
        self.photo = foto
        self.cv = curriculo
        self.create_at = datetime.now()
    
    def get_cpf(self):
        return self.cpf

class Item(Base):
    __tablename__ = 'checklist'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    task = Column(Text) 
    status_of_task = Column(Enum('Em Espera', 'Iniciado', 'Finalizado'))  
    create_at = Column(DateTime)
    final_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'))   

    def __init__(self, tilulo, tarefa, estatus_da_tarefa, data_de_finalizacao, pessoa_id):
        self.title = tilulo
        self.task = tarefa
        self.status_of_task = estatus_da_tarefa
        self.create_at = datetime.now()
        self.final_at = data_de_finalizacao
        self.person_cpf = pessoa_id

engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
Base.metadata.create_all(engine)
