from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from database.db import engine
from models.cube import Cube, CubeCreate, CubeUpdate

router = APIRouter(prefix="/cubes", tags=["Cubes"])



@router.post("/", response_model=Cube)
def create_cube(cube: CubeCreate):
    with Session(engine) as session:
        new_cube = Cube.from_orm(cube)
        session.add(new_cube)
        session.commit()
        session.refresh(new_cube)
        return new_cube



@router.get("/", response_model=List[Cube])
def get_all_cubes():
    with Session(engine) as session:
        cubes = session.exec(select(Cube)).all()
        return cubes



@router.get("/{cube_id}", response_model=Cube)
def get_cube(cube_id: int):
    with Session(engine) as session:
        cube = session.get(Cube, cube_id)
        if not cube:
            raise HTTPException(status_code=404, detail="Cubo no encontrado")
        return cube



@router.put("/{cube_id}", response_model=Cube)
def update_cube(cube_id: int, data: CubeUpdate):
    with Session(engine) as session:
        cube = session.get(Cube, cube_id)
        if not cube:
            raise HTTPException(status_code=404, detail="Cubo no encontrado")

        for key, value in data.dict(exclude_unset=True).items():
            setattr(cube, key, value)

        session.add(cube)
        session.commit()
        session.refresh(cube)
        return cube



@router.delete("/{cube_id}")
def delete_cube(cube_id: int):
    with Session(engine) as session:
        cube = session.get(Cube, cube_id)
        if not cube:
            raise HTTPException(status_code=404, detail="Cubo no encontrado")
        session.delete(cube)
        session.commit()
        return {"message": "Cubo eliminado correctamente ✅"}






