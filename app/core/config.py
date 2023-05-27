from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./db.sqlite'
    secret: str = 'SECRET'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    report_title: str = 'Charity projects report'
    report_range: str = 'A1:J100'
    google_drive_api_version: str = 'v3'
    google_sheets_api_version: str = 'v4'

    class Config:
        env_file = '.env'


settings = Settings()
