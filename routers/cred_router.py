from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Credential, CredentialUpdate

# build REST API
router = APIRouter()  # initialise APIRouter object from fastapi

# request.app.database[X] corresponds to database creds_db.X (aka collection X) where X is some string


@router.post("/", response_description="Create a new credential", status_code=status.HTTP_201_CREATED,
             response_model=Credential)
def create_credential(request: Request, cred: Credential = Body(...)):
    """
    Create a new credential and add it to the database
    """
    cred = jsonable_encoder(cred)
    new_cred = request.app.database["creds"].insert_one(cred)
    created_cred = request.app.database["creds"].find_one(
        {"_id": new_cred.inserted_id}
    )

    return created_cred


@router.get("/", response_description="List all credentials", response_model=list[Credential])
def list_credentials(request: Request):
    creds = list(request.app.database["creds"].find(limit=100))
    return creds


@router.get("/{id}", response_description="Get a single credential by id", response_model=Credential)
def find_credential(id: str, request: Request):
    if (cred := request.app.database["creds"].find_one({"_id": id})) is not None:
        return cred
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credential with ID {id} not found")


@router.put("/{id}", response_description="Update a credential", response_model=Credential)
def update_credential(id: str, request: Request, cred: CredentialUpdate = Body(...)):
    cred = {k: v for k, v in cred.dict().items() if v is not None}  # get the credential to be updated
    if len(cred) >= 1:
        update_result = request.app.database["creds"].update_one(
            {"_id": id}, {"$set": cred}
        )

        if update_result.modified_count == 0:  # failed to update
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credential with ID {id} not found")

    if (
        existing_cred := request.app.database["creds"].find_one({"_id": id})
    ) is not None:
        return existing_cred  # return the updated credential

    # if no credential to be updated OR existing credential is not found, raise exception
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credential with ID {id} not found")


@router.delete("/{id}", response_description="Delete a credential")
def delete_credential(id: str, request: Request, response: Response):
    delete_result = request.app.database["creds"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credential with ID {id} not found")
