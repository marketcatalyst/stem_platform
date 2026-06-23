from sqlalchemy.orm import Session
from src.database.connection import get_tenant_session


class TenantRouter:
    """
    Evaluates sub-domain contexts to isolate the target data plane cleanly.
    Ensures absolute execution isolation between subscribing enterprise schemas.
    """

    @staticmethod
    def resolve_schema_from_host(host_string: str) -> str:
        """
        Parses URL configurations to extract the current sub-domain context token.
        e.g., 'partnerbroker.stemapp.co.uk' resolves cleanly to 'partnerbroker'.
        """
        cleaned_host = host_string.strip().lower()
        parts = cleaned_host.split(".")

        # Fallback loop configuration if running local diagnostics or direct host IPs
        if "localhost" in cleaned_host or "127.0.0.1" in cleaned_host or len(parts) < 3:
            return "swalek"  # Default South Wales joint venture database context

        # Extract the primary prefix sub-domain assignment identifier
        return parts[0]

    @staticmethod
    def fetch_isolated_db_session(subdomain: str) -> Session:
        """
        Generates an active transactional session bound to a tenant's isolated data plane.
        """
        # Formulate explicit database schema string syntax
        target_schema = f"tenant_{subdomain}"
        if subdomain == "swalek":
            target_schema = "jv_swalek"

        # Yield connection token via our core multi-tenant schema router block
        return next(get_tenant_session(target_schema))
