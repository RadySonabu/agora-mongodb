from typing import Optional
from fastapi import  Request, File
from pydantic import BaseModel, Field
import datetime, json

class EventSchema(BaseModel):
    
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    event_title: str = Field(...)
    organizer: str = Field(...)
    interest: str = Field(...)
    focus: str = Field(...)
    venue: str = Field(...)
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    main_event_image: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class EventModel(BaseModel):
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    event_title: Optional[str] = Field(...)
    organizer: Optional[str] = Field(...)
    interest: Optional[str] = Field(...)
    focus: Optional[str] = Field(...)
    venue: Optional[str] = Field(...)
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    main_event_image: Optional[str] = None
    description: Optional[str] = None


class UpdateEventModel(BaseModel):
    active_status: Optional[bool]
    created_by: Optional[str] 
    created_at: Optional[datetime.datetime] 
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    event_title: Optional[str] 
    organizer: Optional[str] 
    interest: Optional[str] 
    focus: Optional[str] 
    venue: Optional[str] 
    start_date: Optional[datetime.date] 
    end_date: Optional[datetime.date] 
    start_time: Optional[datetime.time] 
    end_time: Optional[datetime.time]
    main_event_image: Optional[str] 
    description: Optional[str] 


def PaginatedResponseModel(data, message, count, offset, limit, request: Request ):
    client_host = request.client.host
    
    if offset == 0:
        prev_page = None
    else:
        prev_page = f'{client_host}/?offset={offset}&limit={limit}'

    if int(count) > limit:
        next_page = f'{client_host}/?offset={offset}&limit={limit}'
    else:
        next_page =None
    return {
        "count": count,
        "prev": prev_page,
        "next": next_page,
        "results": data,
    }

def ResponseModel(data, message):
    return data

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}