from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from models import Pessoa  # Supondo que você já tenha definido o modelo Pessoa
from sqlalchemy import create_engine

def conectar_bd():

    try:
    
        engine = create_engine('mysql://root:Jl04081998@127.0.0.1/db_onboarding')
    
        Session = sessionmaker(bind=engine)
    
        return Session()
    
    except SQLAlchemyError as e:
    
        print("Erro ao se conectar com o banco de dados:", e)
    
        return None

def cadastrar(**kwargs):
    
    try:
    
        session = conectar_bd()
    
        if session is not None:
    
            pessoa = Pessoa(**kwargs)
    
            session.add(pessoa)
    
            session.commit()
    
            print("Cadastro realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar pessoa:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()

def login(login, senha):

    try:

        session = conectar_bd()
        
        if session is not None:
        
            query = session.query(Pessoa).filter((Pessoa.email == login) | (Pessoa.cpf == login)).filter(Pessoa.senha == senha)
        
            pessoa = query.one()
        
            return pessoa
    
    except NoResultFound:
    
        print("Combinação de email/cpf e senha não encontrada")
    
    except SQLAlchemyError as e:
    
        print("Erro ao fazer login:", e)
    
    finally:
    
        if session:
    
            session.close()
