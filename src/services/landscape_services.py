
import os
import shutil
from fastapi import FastAPI, Body, File, UploadFile
from fastapi.responses import JSONResponse
import psycopg2

from ..models.landscape_model import LandscapeModel, LandscapeModelCreate, LandscapeModelEdit

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

UPLOAD_DIRECTORY = "D:/repos/FastAPI/fileStorage"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def landscapeListServices(pageSize: int, selectedPage: int) -> JSONResponse:
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
        query = "select * from tbLandscape order by landscape_id limit %s offset %s"
        offset = (selectedPage - 1) * pageSize
        cur.execute(query, (pageSize, offset))
        
        result = cur.fetchall()
        data = []
        for item in result:        
            print(item[0])
            objLandscape = {
                "landscape_id":  item[0],
                "names": item[1],
                "direction": item[2],
                "description": item[3],
                "route": item[4],
                "statusId":  item[5],
                }
            data.append(objLandscape)

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

def searchForLandscapeByIdServices(id: int) -> JSONResponse:
    # This method search for landscape by id
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            port = PORT
        )
        cur = connection.cursor()
        query = "select * from tbLandscape where landscape_id = %s"
        landscape_id = f"{id}"
        cur.execute(query, landscape_id)
        
        result = cur.fetchone()
        objLandscape = {
            "landscape_id":  result[0],
            "names": result[1],
            "direction": result[2],
            "description": result[3],
            "route": result[4],
            "statusId":  result[5],
            }
        if result == None:
            return JSONResponse(content={
                "success": False,
                "message": ERROR_MESSAGE,
                "messageDetail": "No se encontro un paisaje con ese id",
                "data": result
            }, status_code=200)
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": objLandscape
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

def newLandscapeServices(landscape: LandscapeModelCreate) -> JSONResponse:
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
                    INSERT INTO tbLandscape (NAMES, DIRECTION, DESCRIPTION, ROUTE, statusId)
                    VALUES(%s, %s, %s, %s, %s)
                """
        data = (landscape.names.strip(), landscape.direction.strip(), landscape.description.strip(), landscape.route.strip(), ACTIVE)
        #data = (landscape.names.strip(), landscape.direction.strip(), landscape.description.strip(), str(file_location), ACTIVE)
        cur.execute(query, data)
        connection.commit()
        
        print(data)
        
        result = landscape.model_dump()
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

def editLandscapeServices(landscape: LandscapeModelEdit, landscape_id: int) -> JSONResponse:
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
                    update tbLandscape set 
                    NAMES = %s,
                    DIRECTION = %s,
                    DESCRIPTION = %s,
                    ROUTE = %s,
                    statusId = %s
                    where landscape_id = %s
                """
        statusId = str(landscape.statusId)
        id = str(landscape_id)
        data = (
            landscape.names.strip(), 
            landscape.direction.strip(), 
            landscape.description.strip(), 
            landscape.route.strip(), 
            landscape.statusId.strip(), 
            str(id)
            )
        cur.execute(query, data)
        connection.commit()
        
        result = landscape.model_dump()
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

def deleteLandscapeServices(landscape_id: int) -> JSONResponse:
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
                update tbLandscape set statusId = %s
                where landscape_id = %s
                """
        eliminado = 2
        cur.execute(query, (eliminado, str(landscape_id)))
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