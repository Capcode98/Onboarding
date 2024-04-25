from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from app.models.model import Person, Item
from app.models.connectar_bd import connecting_bd
from hashlib import sha256


#________________________________Pessoas___________________________________#

#FUNCIONANDO
def login(login, password):

    '''Faz login de uma pessoa'''

    try:

        session = connecting_bd()
        
        if session is not None:
        
            query = session.query(Person).filter((Person.email == login) | (Person.cpf == login)).filter(Person.password == sha256(password.encode()).digest())
        
            person = query.one()
        
            return person
    
    except NoResultFound:
    
        print("Combinação de email/cpf e senha não encontrada")
    
    except SQLAlchemyError as e:
    
        print("Erro ao fazer login:", e)
    
    finally:
    
        if session:
    
            session.close()


#FUNCIONANDO
def register_person(**kwargs):

    '''Adiciona uma pessoa na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            person = Person(**kwargs)
    
            session.add(person)
    
            session.commit()
    
            print("Cadastro da pessoa realizado com sucesso")
    
    except SQLAlchemyError as e:

        print("Erro ao cadastrar pessoa:", e)

        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()


def edit_person(login1,password1,**kwargs):

    '''Edita um ou mais campos de uma pessoa'''

    try:
        
        session = connecting_bd()

        person = login(login=login1,password=password1)

        for key, value in kwargs.items():

            setattr(person, key, value)

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
def register_item(**kwargs):

    '''Adiciona um item na lista'''
    
    try:
    
        session = connecting_bd()
    
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


def list_itens(id_pessoa):
    
    """Lista todos os itens da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Item).filter(Item.pessoa_id == id_pessoa)
            
            return query.all()
    
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()


def edit_item(id_item, **kwargs):
    
    """Edita os campos de um item da lista"""
    
    session = connecting_bd()
    
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


def dellete_item(id_item):
        
        """Exclui um item da lista"""
        
        session = connecting_bd()
        
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


