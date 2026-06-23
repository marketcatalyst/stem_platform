from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings

# Base class for our relational database models
Base = declarative_base()

# Initialise the core database engine using our validated connection URI
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.DB_POOL_MIN_CONNECTIONS,
    max_overflow=settings.DB_POOL_MAX_CONNECTIONS - settings.DB_POOL_MIN_CONNECTIONS,
    pool_pre_ping=True,  # Automatically verifies connectivity before executing queries
)

# Foundational session factory for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_tenant_session(schema_name: str):
    """
    Generates an isolated database session bound strictly to a tenant's schema.
    Enforces the Module 7 multi-tenant data plane boundary layer.
    """
    session = SessionLocal()
    try:
        # Strict sanitisation: enforce schema names to be purely alphanumeric underscores
        clean_schema = "".join(c for c in schema_name if c.isalnum() or c == "_")

        # Explicitly switch the PostgreSQL search path to the isolated tenant schema
        session.execute(text(f"SET search_path TO {clean_schema};"))
        yield session
    except Exception as e:
        session.rollback()
        print(
            f"[ERROR] Failed to initialise isolated session for schema: {schema_name}"
        )
        raise e
    finally:
        session.close()
