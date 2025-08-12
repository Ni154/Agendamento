from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import venda as venda_model, agendamento as agendamento_model
from ..schemas import venda_schema
from ..config.database import get_db

router = APIRouter(prefix="/vendas", tags=["vendas"])

@router.post("/", response_model=venda_schema.VendaResponse, status_code=status.HTTP_201_CREATED)
def criar_venda(venda: venda_schema.VendaCreate, db: Session = Depends(get_db)):
    total = sum(item.preco * item.quantidade for item in venda.itens)

    nova_venda = venda_model.Venda(
        cliente_id=venda.cliente_id,
        total=total,
        forma_pagamento=venda.forma_pagamento,
        cancelada=False
    )
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)

    for item in venda.itens:
        venda_item = venda_model.VendaItem(
            venda_id=nova_venda.id,
            tipo=item.tipo,
            item_id=item.item_id,
            quantidade=item.quantidade,
            preco=item.preco
        )
        db.add(venda_item)
        # Ajuste de estoque se for produto:
        if item.tipo == "produto":
            produto = db.query(venda_model.Base.classes.produtos).filter_by(id=item.item_id).first()
            if produto:
                produto.quantidade -= item.quantidade
    db.commit()

    return nova_venda

@router.get("/", response_model=List[venda_schema.VendaResponse])
def listar_vendas(db: Session = Depends(get_db)):
    vendas = db.query(venda_model.Venda).filter(venda_model.Venda.cancelada == False).all()
    return vendas

@router.get("/{venda_id}", response_model=venda_schema.VendaResponse)
def obter_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(venda_model.Venda).filter(venda_model.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.post("/pre-venda/{agendamento_id}", response_model=venda_schema.VendaResponse)
def criar_pre_venda(agendamento_id: int, forma_pagamento: str = None, db: Session = Depends(get_db)):
    agendamento = db.query(agendamento_model.Agendamento).filter(agendamento_model.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    # Supondo que agendamento.servicos seja string com nomes ou IDs, adaptar conforme necessário
    # Aqui a lógica para transformar agendamento em venda:
    # por exemplo, cada serviço vira um item do tipo "servico"

    itens = []
    servicos = agendamento.servicos.split(",")  # adaptado se for lista
    for servico_nome in servicos:
        servico_obj = db.query(venda_model.Base.classes.servicos).filter_by(nome=servico_nome.strip()).first()
        if servico_obj:
            itens.append(venda_schema.VendaItemCreate(
                tipo="servico",
                item_id=servico_obj.id,
                quantidade=1,
                preco=servico_obj.valor
            ))
    total = sum(item.preco * item.quantidade for item in itens)

    nova_venda = venda_model.Venda(
        cliente_id=agendamento.cliente_id,
        total=total,
        forma_pagamento=forma_pagamento,
        cancelada=False
    )
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)

    for item in itens:
        venda_item = venda_model.VendaItem(
            venda_id=nova_venda.id,
            tipo=item.tipo,
            item_id=item.item_id,
            quantidade=item.quantidade,
            preco=item.preco
        )
        db.add(venda_item)
    db.commit()

    return nova_venda

@router.put("/{venda_id}/adicionar-item", response_model=venda_schema.VendaResponse)
def adicionar_item(venda_id: int, item: venda_schema.VendaItemCreate, db: Session = Depends(get_db)):
    venda = db.query(venda_model.Venda).filter(venda_model.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    venda_item = db.query(venda_model.VendaItem).filter(
        venda_model.VendaItem.venda_id == venda_id,
        venda_model.VendaItem.tipo == item.tipo,
        venda_model.VendaItem.item_id == item.item_id
    ).first()

    if venda_item:
        venda_item.quantidade += item.quantidade
    else:
        venda_item = venda_model.VendaItem(
            venda_id=venda_id,
            tipo=item.tipo,
            item_id=item.item_id,
            quantidade=item.quantidade,
            preco=item.preco
        )
        db.add(venda_item)

    venda.total += item.preco * item.quantidade
    db.commit()
    db.refresh(venda)

    return venda

@router.post("/{venda_id}/cancelar", status_code=status.HTTP_200_OK)
def cancelar_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(venda_model.Venda).filter(venda_model.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    if venda.cancelada:
        raise HTTPException(status_code=400, detail="Venda já está cancelada")

    venda.cancelada = True
    db.commit()

    # Repor estoque dos produtos
    itens_produtos = db.query(venda_model.VendaItem).filter(
        venda_model.VendaItem.venda_id == venda_id,
        venda_model.VendaItem.tipo == "produto"
    ).all()
    for item in itens_produtos:
        produto = db.query(venda_model.Base.classes.produtos).filter_by(id=item.item_id).first()
        if produto:
            produto.quantidade += item.quantidade
    db.commit()

    return {"detail": f"Venda {venda_id} cancelada com sucesso"}
