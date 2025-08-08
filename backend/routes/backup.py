
from fastapi import APIRouter, Response
import json
from config.database import supabase_client

router = APIRouter(prefix="/backup", tags=["Backup"])

@router.get("/export/json")
async def exportar_backup_json():
    # Lista das tabelas a exportar
    tabelas = ["clientes", "produtos", "servicos", "vendas", "venda_itens", "despesas", "agendamentos"]

    backup_data = {}
    for tabela in tabelas:
        response = supabase_client.table(tabela).select("*").execute()
        if response.error:
            return {"error": f"Erro ao exportar tabela {tabela}: {response.error.message}"}
        backup_data[tabela] = response.data

    json_data = json.dumps(backup_data, ensure_ascii=False, indent=4)

    headers = {
        "Content-Disposition": "attachment; filename=backup_studio_depilation.json"
    }

    return Response(content=json_data, media_type="application/json", headers=headers)
