from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import PersonalDetails, PersonalDetailsUpdate

router = APIRouter()


@router.post("/", response_description="Create a new personal detail types", status_code=status.HTTP_201_CREATED,
             response_model=PersonalDetails)
def create_pdetail(request: Request, cred: PersonalDetails = Body(...)):
    cred = jsonable_encoder(cred)
    new_cred = request.app.database["personal_detail_type"].insert_one(cred)
    created_cred = request.app.database["personal_detail_type"].find_one(
        {"_id": new_cred.inserted_id}
    )
    return created_cred


@router.get("/", response_description="List all personal detail types", response_model=list[PersonalDetails])
def list_pdetails(request: Request):
    creds = list(request.app.database["personal_detail_type"].find(limit=100))
    return creds


@router.get("/{id/name}", response_description="Get a single personal detail type by id",
            response_model=PersonalDetails)
def find_pdetail(pdetail_type_name: str, request: Request):
    if (cred := request.app.database["personal_detail_type"].find_one({"_id": pdetail_type_name})) is not None:
        return cred
    if (cred := request.app.database["personal_detail_type"].find_one({"detail": pdetail_type_name})) is not None:
        return cred
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Personal detail type with ID/name {pdetail_type_name} not found")


@router.put("/{id}", response_description="Update a personal detail type", response_model=PersonalDetails)
def update_pdetail(id: str, request: Request, cred: PersonalDetailsUpdate = Body(...)):
    cred = {k: v for k, v in cred.dict().items() if v is not None}
    if len(cred) >= 1:
        update_result = request.app.database["personal_detail_type"].update_one(
            {"_id": id}, {"$set": cred}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Personal detail type with ID {id} not found")

    if (
        existing_cred := request.app.database["personal_detail_type"].find_one({"_id": id})
    ) is not None:
        return existing_cred

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Personal detail type with ID {id} not found")


@router.delete("/{id}", response_description="Delete a personal detail type")
def delete_pdetail(id: str, request: Request, response: Response):
    delete_result = request.app.database["personal_detail_type"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Personal detail type with ID {id} not found")
