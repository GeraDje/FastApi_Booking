from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_for: date,
            date_to: date,
            has_spa: bool = Query(default=None),
            stars: int = Query(ge=1, le=5, default=None)
    ):
        self.location = location,
        self.date_for = date_for,
        self.date_to = date_to,
        self.has_spa = has_spa,
        self.stars = stars


class SHotels(BaseModel):
    addres:str
    name:str
    stars:int
list_Shotels = list[SHotels]

@app.get("/hotels")
async def get_hotels(
            search_args:HotelsSearchArgs = Depends()
)->list_Shotels:
    hotels = [{
        "addres": "yl. Gagarina, dom 5",
        "name": "Hilton",
        "stars": 5

    }]
    return hotels




class SBookings(BaseModel):
    room_id:int
    date_for:date
    date_to:date
#
# @app.post("/bookings")
# async def add_bookings(bookings:SBookings):
#     pass
#
