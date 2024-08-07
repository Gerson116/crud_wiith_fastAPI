
from fastapi import APIRouter, File, UploadFile

from ..models.landscape_model import LandscapeModel, LandscapeModelCreate, LandscapeModelEdit

from ..services.landscape_services import landscapeListServices, searchForLandscapeByIdServices, newLandscapeServices, editLandscapeServices, deleteLandscapeServices

#Router
ROUTER_Landscape = APIRouter()

@ROUTER_Landscape.get("/landscape-list/{pageSize}/{selectedPage}", tags=["Landscape List"])
def landscapeList(pageSize: int, selectedPage: int):
    resp = landscapeListServices(pageSize, selectedPage)
    return resp

@ROUTER_Landscape.get("/search-for-landscape-by-id/{id}", tags=["Search for landscape by Id"])
def searchForLandscapeById(id: int):
    resp = searchForLandscapeByIdServices(id)
    return resp


@ROUTER_Landscape.post("/new-landscape/", tags=["Add new landscape"])
def newLandscape(landscape: LandscapeModelCreate):
    resp = newLandscapeServices(landscape)
    return resp


@ROUTER_Landscape.put("/edit-landscape/{landscape_id}", tags=["Edit landscape"])
def editLandscape(landscape_id: int, landscape: LandscapeModelEdit):
    print(landscape)
    resp = editLandscapeServices(landscape, landscape_id)
    return resp

@ROUTER_Landscape.delete("/delete-landscape/{landscape_id}", tags=["Delete landscape"])
def deleteLandscape(landscape_id: int):
    resp = deleteLandscapeServices(landscape_id)
    return resp

