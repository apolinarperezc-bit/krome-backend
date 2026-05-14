import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway inyecta DATABASE_URL automáticamente.
# Para desarrollo local usar: postgresql://user:pass@localhost/krome
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./krome_dev.db")

# Railway a veces entrega "postgres://" (viejo), SQLAlchemy necesita "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
