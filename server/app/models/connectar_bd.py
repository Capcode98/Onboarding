from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


def conectar_bd():

    try:
        engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
        Session = sessionmaker(bind=engine)
        return Session()
    
    except SQLAlchemyError as e:
        print("Erro ao se conectar com o banco de dados:", e)
        return None
