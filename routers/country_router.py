from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Country, CountryUpdate

router = APIRouter()


@router.post("/", response_description="Create a new country", status_code=status.HTTP_201_CREATED,
             response_model=Country)
def create_country(request: Request, cred: Country = Body(...)):
    cred = jsonable_encoder(cred)
    new_cred = request.app.database["countries"].insert_one(cred)
    created_cred = request.app.database["countries"].find_one(
        {"_id": new_cred.inserted_id}
    )
    return created_cred


@router.get("/", response_description="List all countries", response_model=list[Country])
def list_countries(request: Request):
    creds = list(request.app.database["countries"].find(limit=100))
    return creds


@router.get("/{id/name}", response_description="Get a single country by ID/name", response_model=Country)
def find_country(country_name: str, request: Request):
    # search for a match with the key, "_id", first
    if (cred := request.app.database["countries"].find_one({"_id": country_name})) is not None:
        return cred
    # else search for match by name
    if (cred := request.app.database["countries"].find_one({"name": country_name})) is not None:
        return cred
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country with ID/name {id} not found")


@router.put("/{id}", response_description="Update a country", response_model=Country)
def update_country(id: str, request: Request, cred: CountryUpdate = Body(...)):
    cred = {k: v for k, v in cred.dict().items() if v is not None}
    if len(cred) >= 1:
        update_result = request.app.database["countries"].update_one(
            {"_id": id}, {"$set": cred}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country with ID {id} not found")

    if (
        existing_cred := request.app.database["countries"].find_one({"_id": id})
    ) is not None:
        return existing_cred

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country with ID {id} not found")


@router.delete("/{id}", response_description="Delete a country")
def delete_country(id: str, request: Request, response: Response):
    delete_result = request.app.database["countries"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country with ID {id} not found")
