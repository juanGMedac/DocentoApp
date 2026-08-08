import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tus credenciales exactas
DB_USER = "ADMIN"
DB_PASSWORD = "***REDACTED***"

# 1. Escapamos los caracteres especiales de tu contraseña (la @)
DB_PASSWORD_ESCAPED = urllib.parse.quote_plus(DB_PASSWORD)

# 2. Tu cadena de conexión "Bajo" (TLS sin Wallet) extraída de tu Oracle Live
ORACLE_CONNECT_STRING = (
    "(description= "
    "(retry_count=20)(retry_delay=3)"
    "(address=(protocol=tcps)(port=1522)(host=adb.eu-madrid-1.oraclecloud.com))"
    "(connect_data=(service_name=g8780a88b7b31da_docentoapp_low.adb.oraclecloud.com))"
    "(security=(ssl_server_dn_match=yes)))"
)

# 3. Construimos la URL base para SQLAlchemy (solo usuario y contraseña)
SQLALCHEMY_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD_ESCAPED}@"

# 4. Creamos el motor pasándole la cadena bajo el nombre correcto 'dsn'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "dsn": ORACLE_CONNECT_STRING
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para proveer una sesión de DB por request en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()