from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)  # Sugestão: usar uma função de hash para armazenar senhas de forma segura
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20))
    endereco = Column(String(255))
    cidade = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100))
    cep = Column(String(9))
    cpf = Column(String(14), unique=True)
    rg = Column(String(20), unique=True)
    data_nascimento = Column(Date)
    sexo = Column(Enum('Masculino', 'Feminino', 'Prefiro Não Declarar'))  # Sugestão: usar ENUM para sexo
    estado_civil = Column(Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'Outro'))
    profissao = Column(String(100))
    salario = Column(DECIMAL(10, 2))  # Sugestão: usar DECIMAL para valores monetários
    escolaridade = Column(Enum('Fundamental', 'Médio', 'Superior', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Outro'))
    idioma = Column(String(100))
    habilidades = Column(Text)  # Sugestão: armazenar habilidades em um formato de texto ou JSON
    experiencia = Column(Text)  # Sugestão: armazenar experiência em um formato de texto ou JSON
    objetivo = Column(Text)  # Sugestão: armazenar objetivo em um formato de texto ou JSON
    foto = Column(String(255))  # Sugestão: armazenar o caminho para a foto, não a foto em si
    curriculo = Column(String(255))  # Sugestão: armazenar o caminho para o currículo, não o currículo em si
    data_de_cadastro = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('cpf','rg', 'email', name='_cpf_rg_email_uc'),  # Garante que tanto CPF quanto email sejam únicos
    )    

    def __init__(self, nome, senha, email, telefone, endereco, cidade, estado, pais, cep, cpf, rg, data_nascimento, sexo, estado_civil, profissao, salario, escolaridade, idioma, habilidades, experiencia, objetivo, foto, curriculo):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.cep = cep
        self.cpf = cpf
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.estado_civil = estado_civil
        self.profissao = profissao
        self.salario = salario
        self.escolaridade = escolaridade
        self.idioma = idioma
        self.habilidades = habilidades
        self.experiencia = experiencia
        self.objetivo = objetivo
        self.foto = foto
        self.curriculo = curriculo
        self.data_de_cadastro = datetime.now()

class Item(Base):
    __tablename__ = 'checklist'

    id = Column(Integer, primary_key=True)
    tilulo = Column(String(100), nullable=False)
    tarefa = Column(Text) 
    estatus_da_tarefa = Column(Enum('Em Espera', 'Iniciado', 'Finalizado'))  
    data_de_criacao = Column(DateTime)
    data_de_finalizacao = Column(DateTime)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))   

    def __init__(self, tilulo, tarefa, estatus_da_tarefa, data_de_finalizacao, pessoa_id):
        self.tilulo = tilulo
        self.tarefa = tarefa
        self.estatus_da_tarefa = estatus_da_tarefa
        self.data_de_criacao = datetime.now()
        self.data_de_finalizacao = data_de_finalizacao
        self.pessoa_id = pessoa_id

engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
Base.metadata.create_all(engine)
