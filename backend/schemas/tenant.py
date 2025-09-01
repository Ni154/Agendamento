from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str
    subdomain: str
    admin_name: str
    admin_email: str
    admin_password: str

class TenantSettingsOut(BaseModel):
    logo_url: str | None = None
    theme_primary: str | None = "#0ea5e9"
    theme_secondary: str | None = "#1f2937"

