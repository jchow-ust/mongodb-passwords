from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Area, AreaUpdate

router = APIRouter()


@router.post("/", response_description="Create a new area", status_code=status.HTTP_201_CREATED,
             response_model=Area)
def create_area(request: Request, cred: Area = Body(...)):
    cred = jsonable_encoder(cred)
    new_cred = request.app.database["areas"].insert_one(cred)
    created_cred = request.app.database["areas"].find_one(
        {"_id": new_cred.inserted_id}
    )
    return created_cred


@router.get("/", response_description="List all areas", response_model=list[Area])
def list_area(request: Request):
    creds = list(request.app.database["areas"].find(limit=100))
    return creds


@router.get("/{id/name}", response_description="Get a single area by ID/name", response_model=Area)
def find_area(area_name: str, request: Request):
    # search for a match with the key, "_id", first
    if (cred := request.app.database["areas"].find_one({"_id": area_name})) is not None:
        return cred
    # else search for match by name
    if (cred := request.app.database["areas"].find_one({"name": area_name})) is not None:
        return cred
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area with ID/name {area_name} not found")


@router.put("/{id}", response_description="Update an area", response_model=Area)
def update_area(id: str, request: Request, cred: AreaUpdate = Body(...)):
    cred = {k: v for k, v in cred.dict().items() if v is not None}
    if len(cred) >= 1:
        update_result = request.app.database["areas"].update_one(
            {"_id": id}, {"$set": cred}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area with ID {id} not found")

    if (
        existing_cred := request.app.database["areas"].find_one({"_id": id})
    ) is not None:
        return existing_cred

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area with ID {id} not found")


@router.delete("/{id}", response_description="Delete an area")
def delete_area(id: str, request: Request, response: Response):
    delete_result = request.app.database["areas"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area with ID {id} not found")
