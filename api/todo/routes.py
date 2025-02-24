from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from auth.dependencies import get_current_user
import models , schemas

todo_router = APIRouter(prefix="/todos", tags=["Todos"])

@todo_router.post("/",response_model=schemas.TodoResponse)
async def create_todo(todo:schemas.TodoCreate, db:AsyncSession = Depends(get_db), email:str=Depends(get_current_user)):
    new_todo = models.Todo(
        user_todo=todo.user_todo,
        completed=todo.completed,
        owner_email=email  # Use the user's email here
    )
    db.add(new_todo)
    await db.commit()
    db.refresh(new_todo)
    return new_todo

@todo_router.get("/", response_model=list[schemas.TodoResponse])
async def get_todos(db:AsyncSession=Depends(get_db), email:str=Depends(get_current_user)):
    result = await db.execute(select(models.Todo).where(models.Todo.owner_email==email))
    todo = result.scalars().all()
    return todo

@todo_router.get("/{todo_id}", response_model=schemas.TodoResponse)
async def get_todo(todo_id:int, db:AsyncSession = Depends(get_db), email:int=Depends(get_current_user)):
    result = await db.execute(select(models.Todo).where(models.Todo.id==todo_id, models.Todo.owner_email==email))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@todo_router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(todo_id: int, updated_todo:schemas.TodoUpdate, db:AsyncSession=Depends(get_db), email:int=Depends(get_current_user)):
    result = await db.execute(select(models.Todo).where(models.Todo.id==todo_id, models.Todo.owner_email==email))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_todo.model_dump().items():
        setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return todo

@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id:int, db:AsyncSession=Depends(get_db), email:int=Depends(get_current_user)):
    result = await db.execute(select(models.Todo).where(models.Todo.id==todo_id, models.Todo.owner_email==email))
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(todo)
    await db.commit()
    return {"message":"Todo deleted successfully"}



