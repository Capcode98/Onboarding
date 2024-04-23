from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Item(Base):
    __tablename__ = 'checklist'

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

    __table_args__ = (
        UniqueConstraint('cpf','rg', 'email', name='_cpf_rg_email_uc'),  # Garante que tanto CPF quanto email sejam únicos
    )

# Substitua 'mysql://user:password@localhost/database' pela sua URL de conexão com o banco de dados MySQL
engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')

Base.metadata.create_all(engine)
