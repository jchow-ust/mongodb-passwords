import uuid
from typing import Optional
from pydantic import BaseModel, Field


# Basic models - Country, Area, PersonalDetails, Mailbox
class Country(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "country_example": {
                "_id": "country01",
                "name": "Hong Kong"
            }
        }


class Mailbox(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    address: str = Field(...)
    desc: str = Field(..., alias="description")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "mailbox_example": {
                "_id": "mbox01",
                "address": "bob.smith@proton.me",
                "description": "For receiving marketing and subscription emails. Rarely opened."
            }
        }


class Area(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    desc: str = Field(..., alias="description")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "area_example": {
                "_id": "area01",
                "title": "Banking",
                "description": "All credentials in this area are for banking or banking-related services."
            }
        }


class PersonalDetails(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    detail: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "pd_example": {
                "_id": "area01",
                "detail": "Date of Birth"
            }
        }


# Other models:
# Credential -> [Country, Area, PersonalDetails, Mailbox]
# JobHuntCredential inherits from Credential
class Credential(BaseModel):  # extend BaseModel from pydantic package
    """
    Initialise the model for the Credential class. This describes all REQUIRED fields
    """
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # auto-populated with universally unique identifier (UUID)
    username: str = Field(...)
    email: str = Field(...)  # from creds_db.mailboxes
    password: str = Field(...)

    country: str = Field(...)  # where the login is relevant (UK, Hong Kong, etc). From creds_db.countries
    area: str = Field(...)  # personal, job hunting, banking, email, etc. From creds_db.areas
    # if != empty str, then this value v denotes that email address v can be used to directly log in to this site
    login_override: str = Field(...)

    # These all use dictionaries since there may be multiple personal details. Stored in key-value pairs in the form:
    # (k,v) where k denotes the detail (e.g. date of birth) and v denotes the value (eg 1996/12/31)
    personal_details: dict[str, str] = Field(...)  # age, DOB, location, card number+PIN, etc.
    security_questions: dict[str, str] = Field(...)

    class Config:
        # example for documentation purposes
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "rt_hon_lettuce_head_mp",
                "password": "pleasebuyadrinkfirst",
                "email": "nevergonnagiveyouup@astley.co.uk",
                "country": "United Kingdom",
                "area": "Banking",
                "login_override": "",
                "personal_details": {"Location": "Oslo, Norway"},
                "security_questions": {"What was the name of your first pet?": "Cthulhu",
                                       "Who was your first kiss?": "Hershey's"}
            }
        }


class JobHuntCredential(Credential):
    """
    Initialise model for JobHuntCredential class, which includes additional fields.
    """
    post_name: str = Field(...)
    contact_person: dict = Field(...)  # may be multiple contact people, so use dict
    expected_salary: tuple[int]  # range of salary. tuple (x, y) denotes salary s such that x ≤ s ≤ y
    reference_number: str = Field(...)
    apply_date: str = Field(...)  # date
    status: str = Field(...)  # PENDING, OFFERED, REJECTED TODO base class?
    medium: str = Field(...)  # where did you find this job post? TODO base class?
    follow_ups: dict = Field(...)  # use dict to store each follow up. key is Date, value is action taken
    # use dict to store. key is Date, value is relevant files (eg interview notes/telephone correspondence)
    follow_up_files: dict = Field(...)

    job_description: str = Field(...)  # stores the job description in text form
    application_details: list[str] = Field(...)  # stores list of files used in application, from cover letters to CVs

    class Config:
        allow_population_by_field_name = True
        # TODO example
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }


# Update classes
class CountryUpdate(BaseModel):
    # don't include 'id' field since that shouldn't be updatable
    name: str

    class Config:
        schema_extra = {
            "country_example": {
                "_id": "country01",
                "name": "Hong Kong"
            }
        }


class MailboxUpdate(BaseModel):
    address: Optional[str]
    desc: Optional[str]

    class Config:
        schema_extra = {
            "mailbox_example": {
                "_id": "mbox01",
                "address": "bob.smith@proton.me",
                "description": "For receiving marketing and subscription emails. Rarely opened."
            }
        }


class AreaUpdate(BaseModel):
    name: Optional[str]
    desc: Optional[str]

    class Config:
        schema_extra = {
            "area_example": {
                "_id": "area01",
                "title": "Banking",
                "description": "All credentials in this Area are for banking or banking-related services."
            }
        }


class PersonalDetailsUpdate(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "pd_example": {
                "_id": "area01",
                "detail": "Date of Birth"
            }
        }


class CredentialUpdate(BaseModel):
    # don't include 'id' field since that shouldn't be updatable
    # optional fields during update
    # TODO
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }


class JobHuntCredentialUpdate(Credential):
    """
    Initialise model for JobHuntCredentialUpdate, which includes additional fields.
    """
    post_name: Optional[str]
    contact_person: Optional[dict]
    expected_salary: Optional[tuple[int]]
    reference_number: Optional[str]
    apply_date: Optional[str]
    status: Optional[str]  # PENDING, OFFERED, REJECTED TODO base class?
    medium: Optional[str]  # where did you find this job post? TODO base class?
    follow_ups: Optional[dict]
    follow_up_files: Optional[dict]
    job_description: Optional[str]  # stores the job description in text form
    application_details: Optional[list[str]]  # stores list of files used in application, from cover letters to CVs

    class Config:
        # TODO example
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }
