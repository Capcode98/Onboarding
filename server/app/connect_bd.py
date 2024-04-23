from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from server.app.models.pessoa_model import Pessoa 
from server.app.models.checklist_model import Item
from sqlalchemy import create_engine

def conectar_bd():

    try:
    
        engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
    
        Session = sessionmaker(bind=engine)
    
        return Session()
    
    except SQLAlchemyError as e:
    
        print("Erro ao se conectar com o banco de dados:", e)
    
        return None

#_____________________________Pessoas________________________________#

def login(login, senha):

    try:

        session = conectar_bd()

        print(f"login: {login} senha: {senha}")
        
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


def cadastrar_Item(**kwargs):
    
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
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()


def editar_pessoa():
    pass

#_____________________________Pessoas________________________________#

def cadastrar_Item(**kwargs):
    
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
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()


def editar_item():
    pass


def excluir_item():
    pass


