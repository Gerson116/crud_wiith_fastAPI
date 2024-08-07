
import bcrypt
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import psycopg2

from ..models.user_model import userModel, userModelCreate, userModelEdit

HOST = "localhost"
DATABASE="DbLandscape"
USER="postgres"
PASSWORD="gsm1020304050"
PORT=5432

SUCCESS_MESSAGE = "Exito"
ERROR_MESSAGE = "Ocurrio un error"
errorMessageDetail = ""
ACTIVE = "1"
INACTIVE = "2"

def userListServices(pageSize: int, selectedPage: int) -> JSONResponse:
    #This method make a consult in the database and return the data with a pagination.
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = "select * from tbUser order by User_id limit %s offset %s"
        offset = (selectedPage - 1) * pageSize
        cur.execute(query, (pageSize, offset))
        
        result = cur.fetchall()
        data = []
        for item in result:        
            print(item[0])
            objUser = {
                "user_id":  item[0],
                "names": item[1],
                "lastname": item[2],
                "email": item[3],
                "statusId":  item[5],
                }
            data.append(objUser)

        return JSONResponse(content={
            "success": True,
            "message": SUCCESS_MESSAGE,
            "data": data
        }, status_code=200)
    except Exception as error:
        errorMessageDetail = error
    finally:
        if cur is not None:
            cur.close()
            connection.close()
    return JSONResponse(content={
            "success": False,
            "message": ERROR_MESSAGE,
            "messageDetail": errorMessageDetail,
            "data": None
        }, status_code=400)

def searchForUserByIdServices(id: int) -> JSONResponse:
    # This method search for User by id
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = "select * from tbUser where user_id = %s"
        user_id = f"{id}"
        cur.execute(query, user_id)
        
        result = cur.fetchone()
        objUser = {
            "user_id":  result[0],
            "names": result[1],
            "lastname": result[2],
            "email": result[3],
            "password":  result[4],
            "statusId":  result[5]
            }
        if result == None:
            return JSONResponse(content={
                "success": False,
                "message": ERROR_MESSAGE,
                "messageDetail": "No se encontro un paisaje con ese id",
                "data": objUser
            }, status_code=200)
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": objUser
        }, status_code=200)
    except Exception as error:
        errorMessageDetail = error
    finally:
        if cur is not None:
            cur.close()
            connection.close()
    return JSONResponse(content={
            "success": False,
            "message": "Ocurrio un Error",
            "messageDetail": errorMessageDetail,
            "data": None
        }, status_code=400)

def encryptPassword(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def decryptPassword(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def newUserServices(User: userModelCreate) -> JSONResponse:
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = """
                    INSERT INTO tbUser (names, lastname, email, password, statusId)
                    VALUES(%s, %s, %s, %s, %s)
                """
        data = (
                User.names.strip(), 
                User.lastname.strip(), 
                User.email.strip(), 
                encryptPassword(User.password.strip()), 
                ACTIVE
                )
        cur.execute(query, data)
        connection.commit()
        
        print(data)
        
        result = User.model_dump()
        successMessageDetail = "Los datos se agregaron con exito"
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "messageDetail": successMessageDetail,
            "data": result
        }, status_code=200)
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
            connection.close()
    return JSONResponse(content={
            "success": False,
            "message": "Ocurrio un Error",
            "messageDetail": errorMessageDetail,
            "data": None
        }, status_code=400)

def editUserServices(user: userModelEdit, user_id: int) -> JSONResponse:
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = """
                    update tbUser set 
                    NAMES = %s,
                    lastname = %s,
                    email = %s,
                    password = %s,
                    statusId = %s
                    where user_id = %s
                """
        statusId = str(user.statusId)
        id = str(user_id)
        data = (
            user.names.strip(), 
            user.lastname.strip(), 
            user.email.strip(), 
            encryptPassword(user.password.strip()), 
            str(user.statusId), 
            str(id)
            )
        cur.execute(query, data)
        connection.commit()
        
        result = user.model_dump()
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": result
        }, status_code=200)
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
            connection.close()
    return JSONResponse(content={
            "success": False,
            "message": "Ocurrio un Error",
            "messageDetail": errorMessageDetail,
            "data": None
        }, status_code=400)

def deleteUserServices(user_id: int) -> JSONResponse:
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = """
                update tbUser set statusId = %s
                where user_id = %s
                """
        eliminado = 2
        cur.execute(query, (eliminado, str(user_id)))
        connection.commit()
        
        result = "respuesta"
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": result
        }, status_code=200)
    except Exception as error:
        errorMessageDetail = error
    finally:
        if cur is not None:
            cur.close()
            connection.close()
    return JSONResponse(content={
            "success": False,
            "message": "Ocurrio un Error",
            "messageDetail": errorMessageDetail,
            "data": None
        }, status_code=400)