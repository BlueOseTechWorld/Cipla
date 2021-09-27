from fastapi.encoders import jsonable_encoder

from pharmaceutical.database import SessionLocal


def convertToJSON(a):
    jsons = []
    for i in a:
        json = jsonable_encoder(i)
        json["values"] = []
        for t, RSD, RTL in zip(json["timeIntervals"].split(','), json["RSD"].split(','), json["RTL"].split(",")):
            json["values"].append([int(t),int(RSD),int(RTL)])
        json.pop("timeIntervals")
        json.pop("RSD")
        json.pop("RTL")
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
    rsd = []
    rtl = []

    for i in values:
        timeIntervals.append(str(i[0]))
        rsd.append(str(i[1]))
        rtl.append(str(i[2]))
    return ",".join(timeIntervals), ",".join(rsd), ",".join(rtl)
