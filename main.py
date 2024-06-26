import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import get_session
from models.ceos import Ceo


# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"
]

app = FastAPI()

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
async def root():
    return {"message": "Hello World"}


@app.post("/ceo/add")
async def create_ceo(ceo_data: Ceo, session: Session = Depends(get_session)):
    # new_ceo = Ceo(name=ceo_data.name, slug=ceo_data.slug, year=ceo_data.year)
    new_ceo = Ceo(**ceo_data.dict())
    session.add(new_ceo)
    session.commit()
    session.refresh(new_ceo)
    return {"CEO added": new_ceo.name}


@app.get('/ceos')
def list_ceos(session: Session = Depends(get_session)):
    statement = select(Ceo).order_by(Ceo.year)
    results = session.exec(statement).all()
    return results


@app.get('/ceos/{slug}')
def get_ceos(slug: str, session: Session = Depends(get_session)):
    statement = select(Ceo).where(Ceo.slug == slug)
    result = session.exec(statement).first()
    return result


@app.put('/ceos/{id}/update')
async def update_ceo(id: int, name: str = None, slug: str = None, year: int = None,  session: Session = Depends(get_session)):
    statement = select(Ceo).where(Ceo.id == id)
    ceo = session.exec(statement).first()
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


@app.delete('/ceos/{id}/delete')
async def remove_ceo(id: int,  session: Session = Depends(get_session)):
    statement = select(Ceo).where(Ceo.id == id)
    ceo = session.exec(statement).first()
    if ceo is not None:
        session.delete(ceo)
        session.commit()
        return {"Deleted CEO": ceo.name}
    else:
        return {"message": "User ID not found"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
