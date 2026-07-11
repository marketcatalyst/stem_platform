import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Tenant(Base):
    """
    Core SaaS Account Profile.
    Tracks distinct white-label brokers or individual corporate clients.
    """

    __tablename__ = "tenants"

    tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False)
    branding_config = Column(
        String, default="{}"
    )  # Dynamically parsed JSON string for themes
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))

    # Relationships
    sites = relationship(
        "ClientSite", back_populates="tenant", cascade="all, delete-orphan"
    )


class AssetTaxonomy(Base):
    """
    The Deterministic 'Worst Offenders' Directory.
    Stores standard electrical signatures and degradation multipliers for un-metered assets.
    """

    __tablename__ = "asset_taxonomy"

    asset_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_class = Column(String(100), nullable=False)
    default_thd_i = Column(Numeric(5, 2), nullable=False)  # Total Harmonic Distortion
    default_cos_phi = Column(Numeric(3, 2), nullable=False)  # Displacement Power Factor
    triplen_harmonic_risk = Column(Boolean, default=False)
    voltage_flicker_risk = Column(Boolean, default=False)
    phase_imbalance_risk = Column(Boolean, default=False)
    thermal_loss_factor = Column(
        Numeric(4, 2), nullable=False
    )  # Arrhenius calculation constant
    description = Column(String, nullable=False)


class ClientSite(Base):
    """
    Tenant-Isolated Operational Facilities.
    Maps localized sites cleanly within a secure multi-tenant boundary.
    """

    __tablename__ = "client_sites"

    site_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        nullable=False,
    )
    client_name = Column(String(255), nullable=False)

    # 🎯 SaaS Robust Fix: Enforce the default value directly on the PostgreSQL server instance
    site_location = Column(
        String(255), nullable=False, server_default=text("'UK Operational Base'")
    )

    # 🎯 SaaS Robust Fix: Enforce a server-side baseline financial limit for onboarding loops
    estimated_annual_spend = Column(
        Numeric(12, 2), nullable=False, server_default=text("0.00")
    )

    main_transformer_kva = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))

    # Relationships
    tenant = relationship("Tenant", back_populates="sites")
    inventories = relationship(
        "SiteInventory", back_populates="site", cascade="all, delete-orphan"
    )


class SiteInventory(Base):
    """
    The 'Rough Twin' Surveyor Checklist Assets.
    Tracks un-metered client assets mapped against standard electrical taxonomies.
    """

    __tablename__ = "site_inventories"

    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(
        UUID(as_uuid=True),
        ForeignKey("client_sites.site_id", ondelete="CASCADE"),
        nullable=False,
    )
    asset_type_id = Column(
        UUID(as_uuid=True), ForeignKey("asset_taxonomy.asset_type_id"), nullable=False
    )
    quantity = Column(Integer, nullable=False, default=1)
    average_kw_rating = Column(Numeric(8, 2), nullable=False)
    duty_cycle_hours_per_week = Column(Numeric(5, 2), nullable=False)
    logged_at = Column(DateTime(timezone=True), server_default=text("NOW()"))

    # Relationships
    site = relationship("ClientSite", back_populates="inventories")
    taxonomy = relationship("AssetTaxonomy")
