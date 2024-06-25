import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our tools
# This is the database connection file
from db_connect import session

# These are our models
from models import CEO, CEOCreate

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Root Route"}

# C


@app.post("/create")
async def create_ceo(ceo_data: CEOCreate):
    ceo = CEO(name=ceo_data.name, slug=ceo_data.slug, year=ceo_data.year)
    session.add(ceo)
    session.commit()
    return {"CEO added": ceo.name}

# R


@app.get('/ceos')
def get_ceos():
    ceos = session.query(CEO)
    return ceos.all()


@app.get('/ceos/{slug}')
def get_ceos(slug: str):
    ceo = session.query(CEO).filter(CEO.slug == slug)
    return ceo.first()

# U


@app.put('/ceos/{id}/update')
async def update_ceo(id: int, name: str = None, slug: str = None, year: int = None):
    ceo = session.query(CEO).filter(CEO.id == id).first()
    if ceo is not None:
        if name:
            ceo.name = name
        if slug:
            ceo.slug = slug
        if year:
            ceo.year = year
        session.add(ceo)
        session.commit()
        return {"Updated CEO": ceo.name}
    else:
        return {"message": "User ID not found"}

# D


@app.delete('/ceos/{id}/delete')
async def remove_ceo(id: int):
    ceo = session.query(CEO).filter(CEO.id == id).first()
    if ceo is not None:
        session.delete(ceo)
        session.commit()
        return {"Deleted CEO": ceo.name}
    else:
        return {"message": "User ID not found"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
