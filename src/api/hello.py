from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src.database import engine
from pydantic import BaseModel


router = APIRouter(
    prefix="/hello",
    tags=["hello"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/hello")
def post_hello():
    return "hello, world!"


class ExampleClass(BaseModel):
    user_id: int
    some_value: str

@router.post("/test_data")
def post_passing_in(request: ExampleClass):
    passed_in_id = request.user_id
    passed_in_value = request.some_value
    return f"passed in id: {passed_in_id}, passed in value {passed_in_value}"

@router.get("/get_from_db")
def post_get_from_db():
    with engine.begin() as connection:
        query = text("SELECT * FROM logtable")
        result = connection.execute(query)
        ans = []
        for row in result:
            print(row)
            ans.append(row._asdict())
        return ans

@router.get("/get_from_db_with_binds")
def post_get_with_binds():
    with engine.begin() as connection:
        query = text("SELECT * FROM logtable WHERE id = :id")
        result = connection.execute(query, {"id": 1})
        ans = []
        for row in result:
            print(row)
            ans.append(row._asdict())
        return ans

class ExamplePost(BaseModel):
    a: int
    b: int

@router.post("/insert_into_db")
def post_insert(request: ExamplePost):
    with engine.begin() as connection:
        query = text("INSERT INTO logtable (a, b) VALUES (:a, :b)")
        connection.execute(query, {"a": request.a, "b": request.b})
    return "OK"