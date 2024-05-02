from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from datetime import datetime


def connecting_bd():

    try:
        engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
        Session = sessionmaker(bind=engine)
        return Session()
    
    except SQLAlchemyError as e:
        print("Erro ao se conectar com o banco de dados:", e)
        return None

def sqlalchemy_to_dict(obj):

    mapper = class_mapper(obj.__class__)
    data = {}

    for column in mapper.columns:
        data[column.key] = getattr(obj, column.key)
    
    return data

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