from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY_SERVICE_ROLE = os.getenv("SUPABASE_KEY_SERVICE_ROLE")
SUPABASE_KEY_PUBLISHABLE = os.getenv("SUPABASE_KEY_PUBLISHABLE")

# Cliente para backend - uso com privilégios completos
supabase_service: Client = create_client(SUPABASE_URL, SUPABASE_KEY_SERVICE_ROLE)

# Cliente para frontend/public - uso limitado
supabase_public: Client = create_client(SUPABASE_URL, SUPABASE_KEY_PUBLISHABLE)
