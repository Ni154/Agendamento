
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from pydantic import BaseModel
from config.database import supabase
from models.venda import VendaModel, VendaItemModel

router = APIRouter(prefix="/vendas", tags=["vendas"])

# Helper para calcular total
def calcular_total(itens: List[VendaItemModel]) -> float:
    return sum(item.preco * item.quantidade for item in itens)

# Criar venda nova
@router.post("/", response_model=VendaModel)
def criar_venda(venda: VendaModel):
    venda.total = calcular_total(venda.itens)
    data_dict = venda.dict()
    itens = data_dict.pop("itens")

    # Inserir venda e pegar id
    response = supabase.table("vendas").insert({
        "cliente_id": data_dict["cliente_id"],
        "data": data_dict["data"].isoformat(),
        "total": venda.total,
        "cancelada": False,
        "forma_pagamento": data_dict.get("forma_pagamento"),
    }).execute()

    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Erro ao criar venda")

    venda_id = response.data[0]["id"]

    # Inserir itens
    itens_db = []
    for item in itens:
        itens_db.append({
            "venda_id": venda_id,
            "tipo": item.tipo,
            "item_id": item.item_id,
            "quantidade": item.quantidade,
            "preco": item.preco
        })

    supabase.table("venda_itens").insert(itens_db).execute()

    venda.id = venda_id
    return venda

# Criar pré-venda a partir de agendamento (só serviços)
@router.post("/pre-venda/{agendamento_id}", response_model=VendaModel)
def criar_pre_venda(agendamento_id: int):
    # Buscar agendamento
    resp = supabase.table("agendamentos").select("*").eq("id", agendamento_id).execute()
    if resp.status_code != 200 or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    agendamento = resp.data[0]

    # Criar venda com dados do agendamento (cliente, data, hora)
    cliente_id = agendamento["cliente_id"]
    data = agendamento["data"]
    servicos_str = agendamento["servicos"]  # string, ex: "depilação, design sobrancelha"
    servicos_lista = [s.strip() for s in servicos_str.split(",") if s.strip()]

    # Buscar ids e preços dos serviços do agendamento (precisa da tabela servicos)
    itens_db = []
    total = 0.0
    for nome_servico in servicos_lista:
        res_s = supabase.table("servicos").select("*").ilike("nome", nome_servico).execute()
        if res_s.status_code == 200 and len(res_s.data) > 0:
            servico = res_s.data[0]
            itens_db.append({
                "tipo": "servico",
                "item_id": servico["id"],
                "quantidade": 1,
                "preco": servico["valor"]
            })
            total += servico["valor"]
        else:
            # Se serviço não encontrado, ignorar ou lançar erro?
            pass

    # Inserir venda
    res_v = supabase.table("vendas").insert({
        "cliente_id": cliente_id,
        "data": data,
        "total": total,
        "cancelada": False,
        "forma_pagamento": None,
    }).execute()
    if res_v.status_code != 201:
        raise HTTPException(status_code=400, detail="Erro ao criar pré-venda")

    venda_id = res_v.data[0]["id"]

    # Inserir itens
    for item in itens_db:
        item["venda_id"] = venda_id
    supabase.table("venda_itens").insert(itens_db).execute()

    # Retornar venda com itens
    venda = VendaModel(
        id=venda_id,
        cliente_id=cliente_id,
        data=date.fromisoformat(data),
        total=total,
        cancelada=False,
        itens=[VendaItemModel(**item) for item in itens_db]
    )
    return venda

# Adicionar itens a uma venda existente (soma quantidade se item já existir)
class ItemAddModel(BaseModel):
    tipo: str  # "produto" ou "servico"
    item_id: int
    quantidade: int = 1
    preco: float

@router.post("/{venda_id}/adicionar-itens", response_model=VendaModel)
def adicionar_itens(venda_id: int, itens_add: List[ItemAddModel]):
    # Buscar itens já existentes da venda
    resp_itens = supabase.table("venda_itens").select("*").eq("venda_id", venda_id).execute()
    if resp_itens.status_code != 200:
        raise HTTPException(status_code=404, detail="Venda não encontrada ou erro ao buscar itens")

    itens_existentes = resp_itens.data

    # Mapear itens existentes para facilitar soma: chave = (tipo, item_id)
    mapa_itens = {}
    for i in itens_existentes:
        chave = (i["tipo"], i["item_id"])
        mapa_itens[chave] = i

    # Atualizar ou inserir os itens da requisição
    for novo_item in itens_add:
        chave = (novo_item.tipo, novo_item.item_id)
        if chave in mapa_itens:
            # Somar quantidade
            item_db = mapa_itens[chave]
            nova_quantidade = item_db["quantidade"] + novo_item.quantidade
            supabase.table("venda_itens").update({"quantidade": nova_quantidade}).eq("id", item_db["id"]).execute()
        else:
            # Inserir novo item
            supabase.table("venda_itens").insert({
                "venda_id": venda_id,
                "tipo": novo_item.tipo,
                "item_id": novo_item.item_id,
                "quantidade": novo_item.quantidade,
                "preco": novo_item.preco
            }).execute()

    # Recalcular total da venda
    resp_totais = supabase.table("venda_itens").select("quantidade, preco").eq("venda_id", venda_id).execute()
    total = 0.0
    if resp_totais.status_code == 200:
        for i in resp_totais.data:
            total += i["quantidade"] * i["preco"]

    # Atualizar total da venda
    supabase.table("vendas").update({"total": total}).eq("id", venda_id).execute()

    # Buscar venda atualizada para retornar
    resp_venda = supabase.table("vendas").select("*").eq("id", venda_id).execute()
    if resp_venda.status_code != 200 or not resp_venda.data:
        raise HTTPException(status_code=404, detail="Venda não encontrada após atualização")
    venda_data = resp_venda.data[0]

    # Buscar itens atualizados
    resp_itens = supabase.table("venda_itens").select("*").eq("venda_id", venda_id).execute()
    itens_list = [VendaItemModel(
        tipo=i["tipo"],
        item_id=i["item_id"],
        quantidade=i["quantidade"],
        preco=i["preco"]) for i in resp_itens.data]

    venda = VendaModel(
        id=venda_data["id"],
        cliente_id=venda_data["cliente_id"],
        data=date.fromisoformat(venda_data["data"]),
        total=venda_data["total"],
        cancelada=venda_data.get("cancelada", False),
        forma_pagamento=venda_data.get("forma_pagamento"),
        itens=itens_list
    )

    return venda

# Buscar todas vendas
@router.get("/", response_model=List[VendaModel])
def listar_vendas():
    resp = supabase.table("vendas").select("*").execute()
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao buscar vendas")

    vendas = []
    for v in resp.data:
        # Buscar itens
        resp_itens = supabase.table("venda_itens").select("*").eq("venda_id", v["id"]).execute()
        itens_list = []
        if resp_itens.status_code == 200:
            for i in resp_itens.data:
                itens_list.append(VendaItemModel(
                    tipo=i["tipo"],
                    item_id=i["item_id"],
                    quantidade=i["quantidade"],
                    preco=i["preco"]
                ))

        venda = VendaModel(
            id=v["id"],
            cliente_id=v["cliente_id"],
            data=date.fromisoformat(v["data"]),
            total=v["total"],
            cancelada=v.get("cancelada", False),
            forma_pagamento=v.get("forma_pagamento"),
            itens=itens_list
        )
        vendas.append(venda)

    return vendas
