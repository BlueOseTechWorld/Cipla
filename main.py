from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.sql.expression import true

app = FastAPI(debug=True)
