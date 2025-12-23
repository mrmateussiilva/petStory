"""Payment storage using SQLModel database."""

import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from contextlib import contextmanager

from sqlmodel import Session, select

from app.core.database import engine
from app.models.payment import Payment

logger = logging.getLogger(__name__)


class PaymentStorage:
    """Database-backed payment storage using SQLModel.
    
    Persists payment information to database for production use.
    """

    def __init__(self):
        """Initialize payment storage."""
        # Cleanup old entries periodically (older than 7 days)
        self._cleanup_threshold = timedelta(days=7)

    @contextmanager
    def _get_session(self):
        """Get a database session context manager."""
        with Session(engine) as session:
            yield session

    def save_payment(
        self,
        payment_id: str,
        status: str,
        email: str,
        pet_name: Optional[str] = None,
        external_reference: Optional[str] = None,
    ) -> None:
        """Save payment information.
        
        Args:
            payment_id: Mercado Pago payment ID
            status: Payment status (approved, pending, rejected, etc.)
            email: Customer email
            pet_name: Pet name (optional)
            external_reference: External reference from Mercado Pago
        """
        with self._get_session() as session:
            # Check if payment already exists
            existing = session.exec(
                select(Payment).where(Payment.payment_id == payment_id)
            ).first()
            
            if existing:
                # Update existing payment
                existing.status = status
                existing.email = email
                existing.pet_name = pet_name
                existing.external_reference = external_reference
                existing.updated_at = datetime.now()
                session.add(existing)
                logger.info(f"Updated payment {payment_id} with status {status}")
            else:
                # Create new payment
                payment = Payment(
                    payment_id=payment_id,
                    status=status,
                    email=email,
                    pet_name=pet_name,
                    external_reference=external_reference,
                )
                session.add(payment)
                logger.info(f"Saved new payment {payment_id} with status {status} for {email}")
            
            session.commit()

    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """Get payment information.
        
        Args:
            payment_id: Mercado Pago payment ID
            
        Returns:
            Payment information dictionary or None
        """
        with self._get_session() as session:
            payment = session.exec(
                select(Payment).where(Payment.payment_id == payment_id)
            ).first()
            
            if payment:
                return {
                    "status": payment.status,
                    "email": payment.email,
                    "pet_name": payment.pet_name,
                    "timestamp": payment.created_at,
                    "external_reference": payment.external_reference,
                }
            return None

    def get_payment_by_reference(self, external_reference: str) -> Optional[Dict]:
        """Get payment by external reference.
        
        Args:
            external_reference: External reference from Mercado Pago
            
        Returns:
            Payment information dictionary or None
        """
        with self._get_session() as session:
            payment = session.exec(
                select(Payment).where(Payment.external_reference == external_reference)
            ).first()
            
            if payment:
                return {
                    "status": payment.status,
                    "email": payment.email,
                    "pet_name": payment.pet_name,
                    "timestamp": payment.created_at,
                    "external_reference": payment.external_reference,
                }
            return None

    def is_payment_approved(self, payment_id: str) -> bool:
        """Check if payment is approved.
        
        Args:
            payment_id: Mercado Pago payment ID
            
        Returns:
            True if payment is approved, False otherwise
        """
        payment = self.get_payment(payment_id)
        if payment:
            return payment["status"] == "approved"
        return False

    def can_upload(self, email: str, pet_name: str) -> bool:
        """Check if user can upload (has approved payment).
        
        Args:
            email: Customer email
            pet_name: Pet name
            
        Returns:
            True if user has an approved payment for this pet, False otherwise
        """
        with self._get_session() as session:
            # Find approved payment for this email and pet within last 24 hours
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            payment = session.exec(
                select(Payment)
                .where(Payment.email == email)
                .where(Payment.pet_name == pet_name)
                .where(Payment.status == "approved")
                .where(Payment.created_at >= cutoff_time)
            ).first()
            
            return payment is not None

    def cleanup_old_payments(self) -> None:
        """Remove payments older than cleanup threshold."""
        with self._get_session() as session:
            cutoff_time = datetime.now() - self._cleanup_threshold
            
            old_payments = session.exec(
                select(Payment).where(Payment.created_at < cutoff_time)
            ).all()
            
            count = 0
            for payment in old_payments:
                session.delete(payment)
                count += 1
            
            session.commit()
            
            if count > 0:
                logger.info(f"Cleaned up {count} old payment records")


# Global instance
payment_storage = PaymentStorage()

