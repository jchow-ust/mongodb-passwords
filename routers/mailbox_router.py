from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Mailbox, MailboxUpdate

router = APIRouter()


@router.post("/", response_description="Create a new mailbox", status_code=status.HTTP_201_CREATED,
             response_model=Mailbox)
def create_mailbox(request: Request, cred: Mailbox = Body(...)):
    cred = jsonable_encoder(cred)
    new_cred = request.app.database["mailboxes"].insert_one(cred)
    created_cred = request.app.database["mailboxes"].find_one(
        {"_id": new_cred.inserted_id}
    )
    return created_cred


@router.get("/", response_description="List all mailboxes", response_model=list[Mailbox])
def list_mailboxes(request: Request):
    creds = list(request.app.database["mailboxes"].find(limit=100))
    return creds


@router.get("/{id/address}", response_description="Get a single mailbox by ID or that mailbox's address",
            response_model=Mailbox)
def find_mailbox(mailbox: str, request: Request):
    if (cred := request.app.database["mailboxes"].find_one({"_id": mailbox})) is not None:
        return cred
    if (cred := request.app.database["mailboxes"].find_one({"address": mailbox})) is not None:
        return cred
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mailbox with ID/name {mailbox} not found")


@router.put("/{id}", response_description="Update a mailbox", response_model=Mailbox)
def update_mailbox(id: str, request: Request, cred: MailboxUpdate = Body(...)):
    cred = {k: v for k, v in cred.dict().items() if v is not None}
    if len(cred) >= 1:
        update_result = request.app.database["mailboxes"].update_one(
            {"_id": id}, {"$set": cred}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mailbox with ID {id} not found")

    if (
        existing_cred := request.app.database["mailboxes"].find_one({"_id": id})
    ) is not None:
        return existing_cred

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mailbox with ID {id} not found")


@router.delete("/{id}", response_description="Delete a mailbox")
def delete_mailbox(id: str, request: Request, response: Response):
    delete_result = request.app.database["mailboxes"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mailbox with ID {id} not found")
