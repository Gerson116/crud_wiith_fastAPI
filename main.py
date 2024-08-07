from fastapi import FastAPI, APIRouter
from src.controllers.login_controller import ROUTER_Login
from src.controllers.landscape_controller import ROUTER_Landscape
from src.controllers.register_controller import ROUTER_Register

# from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="log-in")

app = FastAPI()
app.include_router(router=ROUTER_Login)
app.include_router(router=ROUTER_Landscape)
app.include_router(router=ROUTER_Register)



