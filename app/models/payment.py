"""Payment model for database."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Payment(SQLModel, table=True):
    """Payment record model.
    
    Stores payment information from Mercado Pago.
    """
    
    __tablename__ = "payments"
    
    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Mercado Pago payment ID (unique)
    payment_id: str = Field(unique=True, index=True)
    
    # Payment status (approved, pending, rejected, cancelled, etc.)
    status: str = Field(index=True)
    
    # Customer information
    email: str = Field(index=True)
    pet_name: Optional[str] = Field(default=None, index=True)
    
    # External reference from Mercado Pago
    external_reference: Optional[str] = Field(default=None, index=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

