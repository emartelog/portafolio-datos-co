import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("config/.env")

def conectar():
    DB_NAME     = os.getenv("DB_NAME")
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = os.getenv("DB_PORT")

    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    return engine

if __name__ == "__main__":
    engine = conectar()
    with engine.connect() as conn:
        resultado = conn.execute(text('SELECT COUNT(*) FROM "OCUPADOS_GEIH"'))
        filas = resultado.fetchone()[0]
        print(f"✅ Conexión exitosa — OCUPADOS_GEIH tiene {filas:,} filas")