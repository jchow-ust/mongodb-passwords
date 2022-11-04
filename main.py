from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

from routers.cred_router import router as c_router
from routers.country_router import router as c2_router
from routers.pdetail_router import router as p_router
from routers.mailbox_router import router as m_router
from routers.area_router import router as a_router


# using connection string in .env file (with username and password), login to our MongoDB
config = dotenv_values(".env")

app = FastAPI()


# event handler to connect to Atlas cluster when application starts
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")  # should see this message if successfully connected


# event handler to disconnect from Atlas cluster when application ends
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


# add router for each collection
app.include_router(c_router, tags=["creds"], prefix="/cred")
app.include_router(m_router, tags=["mailboxes"], prefix="/mailbox")
app.include_router(a_router, tags=["areas"], prefix="/area")
app.include_router(p_router, tags=["personal_detail_types"], prefix="/personal_detail_types")
app.include_router(c2_router, tags=["countries"], prefix="/country")
