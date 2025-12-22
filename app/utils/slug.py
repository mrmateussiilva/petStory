"""Utility functions for generating slugs."""

import re
from datetime import datetime


def email_to_slug(email: str) -> str:
    """Convert email address to a filesystem-safe slug.
    
    Args:
        email: Email address (e.g., "user@example.com")
        
    Returns:
        Slug string (e.g., "user-example-com")
    """
    # Remove everything except alphanumeric, dots, and @
    # Replace @ with dash
    slug = email.lower().strip()
    slug = slug.replace("@", "-")
    slug = slug.replace(".", "-")
    
    # Remove any characters that aren't alphanumeric or dash
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    
    # Remove multiple consecutive dashes
    slug = re.sub(r"-+", "-", slug)
    
    # Remove leading/trailing dashes
    slug = slug.strip("-")
    
    return slug


def get_user_backup_dir(base_dir: str, email: str) -> str:
    """Get backup directory path for a user based on email.
    
    Args:
        base_dir: Base directory for backups
        email: User email address
        
    Returns:
        Full path to user's backup directory
    """
    slug = email_to_slug(email)
    return f"{base_dir}/{slug}"

