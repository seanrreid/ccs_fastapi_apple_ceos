import uvicorn
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from db import get_session
from models.ceos import Ceo

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add Session dependency from db file
@app.get('/ceos')
def list_ceos(session: Session = Depends(get_session)):
    statement = select(Ceo)
    results = session.exec(statement).all()
    return results


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
