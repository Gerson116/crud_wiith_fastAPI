
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..models.login_model import loginModel
from ..services.login_services import loginServices, create_access_token

#Router
ROUTER_Login = APIRouter()

@ROUTER_Login.post("/log-in", tags=["Log in"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "gerson.santosm3@gmail.com" and form_data.password == "gsm1020304050":
        
        return JSONResponse(content={
            "success": True,
            "message": "Exito",
            "data": {
                "access_token": create_access_token({
                    "username": form_data.username
                }),
                "token_type": "bearer"
            },
        }, status_code=200)
    
    return Response(status_code= 400)