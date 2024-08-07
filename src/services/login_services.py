
from datetime import datetime, timedelta
import bcrypt
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse
import jwt
import psycopg2

from ..models.login_model import loginModel

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

SECRET_KEY = "aquiElKeyDeMiToken"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def decryptPassword(password: str, hashed_password: str):
    hashed_password_bytes = bytes.fromhex(hashed_password[2:])
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def loginServices() -> JSONResponse:
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
        query = "SELECT * FROM tbUser WHERE email = %s"
        email = userInfo.email
        cur.execute(query, (userInfo.email,))
        
        result = cur.fetchone()

        if result is None:
            return JSONResponse(content={
                "success": False,
                "message": ERROR_MESSAGE,
                "messageDetail": "",
                "data": objUser
            }, status_code=401, detail="Invalid credentials")
        
        objUser = {
            "user_id": result[0],
            "names": result[1],
            "lastname": result[2],
            "email": result[3],
            "password": result[4],
            "statusId": result[5]
            }
        
        print(objUser)
        validPass = decryptPassword(userInfo.password, result[4])
        print(validPass)
        # print(validPass)

        if validPass == False:
            return JSONResponse(content={
                "success": False,
                "message": ERROR_MESSAGE,
                "messageDetail": "Inicio de sesion invalido",
                "data": objUser
            }, status_code=401, detail="Invalid credentials")
        
        if result == None:
            return JSONResponse(content={
                "success": False,
                "message": ERROR_MESSAGE,
                "messageDetail": "No se encontro un paisaje con ese id",
                "data": objUser
            }, status_code=400)
        
        access_token = create_access_token(data={"sub": userInfo.email})
        print(access_token)
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": objUser,
            "access_token": access_token, 
            "token_type": "bearer"
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
