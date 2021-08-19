from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from starlette.status import HTTP_200_OK
from pharmaceutical import schemas
from . import models
from .database import engine
from .models import Methods, Batches
from .utils import convertToJSON, get_db, convertFromJSON
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

models.Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1 creating the Method
@app.post('/methods', status_code=status.HTTP_201_CREATED)
def methods(request: schemas.Methods, db: Session = Depends(get_db)):
    print(request)
    new_method = Methods(date=request.date, name=request.name,
                         comment=request.comment, media=request.media,
                         surfactant=request.surfactant, conc=request.conc,
                         volume=request.volume, apparatus=request.apparatus,
                         speed=request.speed, N=request.N)
    db.add(new_method)
    db.commit()
    db.refresh(new_method)
    print(new_method)
    return new_method

# 2 To Show All Methods
@app.get("/methods", status_code=status.HTTP_200_OK)
def methods(db: Session = Depends(get_db)):
    return db.query(models.Methods).all()

# 3 To Show Single Method
@app.get("/methods/{method_id}", status_code=status.HTTP_200_OK)
def methods(method_id: int, db: Session = Depends(get_db)):
    method = db.query(models.Methods).where(models.Methods.id == method_id).first()
    if not method:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Method Not Found')
    return method

# 4 Updating Method
@app.put("/methods/{id}", status_code=status.HTTP_200_OK)
def methods(method_id: int, request: schemas.MethodsUpdate, db: Session = Depends(get_db)):
    exp = db.query(models.Methods).filter(models.Methods.id == method_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Method Not Found')
    print(dict(request))
    db.query(models.Methods).filter(models.Methods.id == method_id).update(dict(request))
    db.commit()

    return db.query(models.Methods).where(models.Methods.id == method_id).first()

# 5 delete method
@app.delete("/methods/{method_id}", status_code=status.HTTP_200_OK)
def methods(id: int, db: Session = Depends(get_db)):
    det = db.query(models.Methods).filter(models.Methods.id == id).first()
    if not det:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Method not found')
    db.query(models.Methods).filter(models.Methods.id ==
                                    id).delete(synchronize_session=False)
    db.query(models.Batches).filter(models.Batches.methodId ==
                                    id).delete(synchronize_session=False)
    db.commit()
    return {"detail": "Method deleted Sucessfully"}

# 6 To Create New Batch For Method
@app.post("/methods/{id}/batches", status_code=status.HTTP_201_CREATED)
def batches(request: schemas.Batches, method_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Methods).filter(models.Methods.id == method_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Method Not Found')
    timeIntervals, measurement = convertFromJSON(request.values)
    new_batch = Batches(batchNumber=request.batchNumber, timeIntervals=timeIntervals,
                        measurement=measurement, methodId=method_id)

    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

# 7 Fetch All Batches
@app.get("/batches", status_code=status.HTTP_200_OK)
def batches(db: Session = Depends(get_db)):
    a = convertToJSON(db.query(models.Batches).all())
    return a

# 8 Fetch a single batch
@app.get("/methods/{method_id}/batches/{batch_id}", status_code=HTTP_200_OK)
def batches(method_id: int, batch_id: int,db: Session = Depends(get_db)):
    a=db.query(models.Batches).filter(models.Batches.methodId == method_id).filter(models.Batches.id == batch_id).first()
    print(a)
    return a

# 8 Updating Batch
@app.put("/batches/{id}", status_code=status.HTTP_200_OK)
def batches(batch_id: int, request: schemas.Batches, db: Session = Depends(get_db)):
    exp = db.query(models.Batches).filter(
        models.Batches.id == batch_id).first()
    if not exp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Method Not Found')
    timeIntervals, measurement = convertFromJSON(request.values)
    upt_batch = Batches(batchNumber=request.batchNumber, timeIntervals=timeIntervals,
                        measurement=measurement)
    amn = db.query(models.Batches).filter(
        models.Batches.id == batch_id).update({'batchNumber': request.batchNumber, 'timeIntervals': timeIntervals,
                                              'measurement': measurement})
    db.commit()
    return db.query(models.Batches).where(models.Batches.id == batch_id).first()

# 9 delete batch
@app.delete("methods/{method_id}/batches/{batch_id}", status_code=status.HTTP_200_OK)
def batches(id: int, db: Session = Depends(get_db)):
    delt = db.query(models.Batches).filter(models.Batches.id == id).first()
    if not delt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Batch not found')

    db.query(models.Batches).filter(models.Batches.id ==
                                    id).delete(synchronize_session=False)
    db.commit()
    return {"detail": "Batch deleted Sucessfully"}

# 10 To Get Batch For Single Method
@app.get("/methods/{method_id}/batches", status_code=status.HTTP_200_OK)
def batches(method_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Methods).filter(
        models.Methods.id == method_id).first()
    if not exp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Method Not Found')
    a = convertToJSON(db.query(models.Batches).where(
        models.Batches.methodId == method_id).all())
    return a





