from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from app.models.model import Pessoa, Item
from app.models.connectar_bd import conectar_bd
from sqlalchemy import create_engine


#________________________________Pessoas___________________________________#

#FUNCIONANDO
def login(login, senha):

    '''Faz login de uma pessoa'''

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


#FUNCIONANDO
def cadastrar_pessoa(**kwargs):

    '''Adiciona uma pessoa na lista'''
    
    try:
    
        session = conectar_bd()
    
        if session is not None:
    
            pessoa = Pessoa(**kwargs)
    
            session.add(pessoa)
    
            session.commit()
    
            print("Cadastro da pessoa realizado com sucesso")
    
    except SQLAlchemyError as e:

        print("Erro ao cadastrar pessoa:", e)

        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()


def editar_pessoas(login1,senha1,**kwargs):

    '''Edita um ou mais campos de uma pessoa'''

    try:
        
        session = conectar_bd()

        pessoa = login(login=login1,senha=senha1)

        for key, value in kwargs.items():

            setattr(pessoa, key, value)

        session.commit()

        print("Pessoa editada com sucesso")
    
    except Exception as e:
    
        print("Erro ao editar pessoa:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()


#_____________________________Item_da_Lista________________________________#

#FUNCIONANDO
def cadastrar_item(**kwargs):

    '''Adiciona um item na lista'''
    
    try:
    
        session = conectar_bd()
    
        if session is not None:
    
            item = Item(**kwargs)
    
            session.add(item)
    
            session.commit()
    
            print("Cadastro do item realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao item pessoa:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()


def listar_itens(id_pessoa):
    
    """Lista todos os itens da lista"""
    
    session = conectar_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Item).filter(Item.pessoa_id == id_pessoa)
            
            return query.all()
    
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()


def editar_item(id_item, **kwargs):
    
    """Edita os campos de um item da lista"""
    
    session = conectar_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Item).filter(Item.id == id_item)
    
            item = query.one()
    
            for key, value in kwargs.items():
    
                setattr(item, key, value)
    
            session.commit()
    
            print("Item editado com sucesso")
    
    except NoResultFound:
    
        print("Item não encontrado")
    
    except Exception as e:
    
        print("Erro ao editar item:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()


def excluir_item(id_item):
        
        """Exclui um item da lista"""
        
        session = conectar_bd()
        
        try:
        
            if session is not None:
        
                query = session.query(Item).filter(Item.id == id_item)
        
                item = query.one()
        
                session.delete(item)
        
                session.commit()
        
                print("Item excluído com sucesso")
        
        except NoResultFound:
        
            print("Item não encontrado")
        
        except Exception as e:
        
            print("Erro ao excluir item:", e)
        
            session.rollback()
        
        finally:
        
            if session:
        
                session.close()


