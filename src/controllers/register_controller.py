
from fastapi import APIRouter, Depends

from ..services.user_services import userListServices, searchForUserByIdServices, newUserServices, editUserServices, deleteUserServices
from ..models.user_model import userModel, userModelCreate, userModelEdit
from ..utils.consts import oauth2_scheme

#Router
ROUTER_Register = APIRouter()

@ROUTER_Register.get("/user-list/{pageSize}/{selectedPage}", tags=["user List"])
def userList(pageSize: int, selectedPage: int):
    resp = userListServices(pageSize, selectedPage)
    return resp

@ROUTER_Register.get("/search-for-user-by-id/{id}", tags=["Search for user by Id"])
def searchForUserById(id: int):
    resp = searchForUserByIdServices(id)
    return resp


@ROUTER_Register.post("/new-user/", tags=["Add new user"])
def newUser(user: userModelCreate, token: str = Depends(oauth2_scheme)):
    resp = newUserServices(user)
    return resp


@ROUTER_Register.put("/edit-user/{user_id}", tags=["Edit user"])
def editUser(user_id: int, user: userModelEdit):
    print(user)
    resp = editUserServices(user, user_id)
    return resp

@ROUTER_Register.delete("/delete-user/{user_id}", tags=["Delete user"])
def deleteUser(user_id: int):
    resp = deleteUserServices(user_id)
    return resp

