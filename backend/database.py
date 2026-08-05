import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno desde el archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DSN = os.getenv("DB_DSN", "localhost:1521/XEPDB1")
WALLET_LOCATION = os.getenv("WALLET_LOCATION")
WALLET_PASSWORD = os.getenv("WALLET_PASSWORD")

# Configuración para Oracle Database utilizando el driver python-oracledb
# Formato típico: oracle+oracledb://usuario:password@dsn
SQLALCHEMY_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_DSN}"

# Configuración adicional de conexión para mTLS con Wallet
connect_args = {}
if WALLET_LOCATION and WALLET_PASSWORD:
    connect_args = {
        "wallet_location": WALLET_LOCATION,
        "wallet_password": WALLET_PASSWORD
    }

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
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
