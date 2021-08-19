from fastapi.encoders import jsonable_encoder

from pharmaceutical.database import SessionLocal


def convertToJSON(a):
    jsons = []
    for i in a:
        json = jsonable_encoder(i)
        json["values"] = dict(
            zip(json["timeIntervals"].split(','), json["measurement"].split(',')))
        jsons.append(json)
    return jsons


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def convertFromJSON(values):
    timeIntervals = []
    measurement = []
    for k, v in values.items():
        timeIntervals.append(str(k))
        measurement.append(str(v))
    return ",".join(timeIntervals), ",".join(measurement)
