from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


def connecting_bd():

    try:
        engine = create_engine('mysql+mysqlconnector://root:Jl04081998@localhost/db_onboarding')
        Session = sessionmaker(bind=engine)
        return Session()
    
    except SQLAlchemyError as e:
        print("Erro ao se conectar com o banco de dados:", e)
        return None

def sqlalchemy_to_dict(obj):
    # Obtém o mapeamento da classe SQLAlchemy
    mapper = class_mapper(obj.__class__)
    # Inicializa um dicionário vazio para armazenar os atributos
    data = {}
    # Itera sobre cada coluna do mapeamento
    for column in mapper.columns:
        # Adiciona o nome da coluna e o valor correspondente ao dicionário
        data[column.key] = getattr(obj, column.key)
    print(data)
    return data