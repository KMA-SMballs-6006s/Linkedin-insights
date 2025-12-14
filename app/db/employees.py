from app.db import mongo 

async def insert_employees(employees: list[dict]):
    if not employees or mongo.db is None:
        return
    await mongo.db.employees.insert_many(employees)