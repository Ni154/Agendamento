from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/backup", tags=["backup"])

# Caminho do arquivo de backup (ajuste se necessário)
BACKUP_PATH = "backup/studio_depilation_backup.sql"

@router.get("/download", response_class=FileResponse, status_code=status.HTTP_200_OK)
def baixar_backup():
    if not os.path.exists(BACKUP_PATH):
        return Response(content="Backup não encontrado", status_code=404)
    return FileResponse(BACKUP_PATH, filename="studio_depilation_backup.sql", media_type="application/octet-stream")
