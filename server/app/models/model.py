from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, UniqueConstraint, ForeignKey, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from hashlib import sha256
from datetime import datetime

Base = declarative_base()

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

def virify_date(data_menor,data_maior,param):
    data_maior=datetime.strptime(data_maior, "%Y-%m-%d %H:%M:%S")
    if param == "finalização":
        data_menor = datetime.strptime(data_menor, "%Y-%m-%d %H:%M:%S")
        if data_menor <= data_maior:
            return data_maior
        else:
            raise ValueError(f"Data de {param} menor que a data de início da tarefa")
    else:
        if data_menor <= data_maior:
            return data_maior
        else:
            raise ValueError(f"Data de {param} menor que a data de criação da tarefa")

class Item(Base):
    __tablename__ = 'checklist'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    task = Column(Text) 
    status_of_task = Column(Enum('Em Espera', 'Iniciado', 'Finalizado'))  
    create_at = Column(DateTime)
    init_at = Column(DateTime)
    finish_at = Column(DateTime)
    person_cpf = Column(String(14), ForeignKey('pessoas.cpf'), nullable=False)   

    #tirar isso, pq assim outros usuarios não poderam ter tarefas com o mesmo nome mesmo que as tarefas existentes sejam de outro usuario
    __table_args__ = (
        UniqueConstraint('title', name='_title_uc'),  # Garante que o titulo seja único
    )  

    def __init__(self, tilulo, tarefa, estatus_da_tarefa, data_de_inicio, data_de_finalizacao, pessoa_id):
        self.title = tilulo
        self.task = tarefa
        self.status_of_task = estatus_da_tarefa
        self.create_at = datetime.now()
        self.init_at = virify_date(data_menor=datetime.now(),data_maior=data_de_inicio,param="início")
        self.finish_at = virify_date(data_menor=data_de_inicio,data_maior=data_de_finalizacao,param="finalização")
        self.person_cpf = pessoa_id

    
    
engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
Base.metadata.create_all(engine)
