from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas.produto_schema import ProdutoCreate, ProdutoOut, ProdutoUpdate
from ..models.produto import Produto
from ..config.database import get_db

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.nome == produto.nome).first()
    if db_produto:
        raise HTTPException(status_code=400, detail="Produto já existe")
    novo_produto = Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=List[ProdutoOut])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    return produtos

@router.get("/{produto_id}", response_model=ProdutoOut)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: int, produto_atualizado: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    update_data = produto_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return None
