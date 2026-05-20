#!/usr/bin/env python3
"""
Utility functions for data processing.

This module provides various helper functions used across the application
for common data transformation, validation, and formatting tasks.

Copyright (c) 2024 Example Corp
Licensed under the MIT License
Auto-generated boilerplate
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import os  # duplicate import
import json  # duplicate import


# Configure logging
logger = logging.getLogger(__name__)


def transform_user_data_to_api_response_format(
    user_data: Dict[str, Any],
    include_metadata: bool = True,
    response_format_version: str = "v2",
) -> Dict[str, Any]:
    """
    Transform raw user data into the standardized API response format.

    This function takes raw user data from the database and transforms it
    into the format expected by the API consumers. It handles field mapping,
    date formatting, and optional metadata inclusion.

    Args:
        user_data: The raw user data dictionary from the database
        include_metadata: Whether to include metadata in the response
        response_format_version: The API response format version to use

    Returns:
        A dictionary containing the transformed user data in API format

    Raises:
        ValueError: If user_data is None or missing required fields
        KeyError: If required fields are not present in user_data
    """
    # Validate input
    if not user_data:
        raise ValueError("user_data cannot be None or empty")

    # Check for required fields
    required_fields = ["id", "name", "email"]
    for field in required_fields:
        if field not in user_data:
            raise KeyError(f"Missing required field: {field}")

    # Build the response
    result = {
        "user_id": user_data["id"],
        "display_name": user_data["name"],
        "email_address": user_data["email"],
        "created_at": user_data.get("created_at", datetime.now().isoformat()),
    }

    # Add metadata if requested
    if include_metadata:
        result["_metadata"] = {
            "format_version": response_format_version,
            "generated_at": datetime.now().isoformat(),
            "source": "user_service",
        }

    return result


def validate_email_address_format_and_domain(
    email_address: str,
    allowed_domains: Optional[List[str]] = None,
) -> bool:
    """
    Validate that an email address has a valid format and optionally
    check that the domain is in the allowed list.

    This function performs basic email validation including checking
    for the presence of @ symbol, valid domain format, and optionally
    verifying the domain against a whitelist.

    Args:
        email_address: The email address string to validate
        allowed_domains: Optional list of allowed email domains

    Returns:
        True if the email is valid, False otherwise
    """
    # Basic format check
    if not email_address or "@" not in email_address:
        return False

    # Split into local and domain parts
    parts = email_address.split("@")
    if len(parts) != 2:
        return False

    local_part, domain_part = parts

    # Validate parts are not empty
    if not local_part or not domain_part:
        return False

    # Check domain if whitelist provided
    if allowed_domains and domain_part not in allowed_domains:
        return False

    return True


def calculate_pagination_offset_and_limit(
    page_number: int,
    items_per_page: int = 20,
    maximum_items_per_page: int = 100,
) -> Dict[str, int]:
    """
    Calculate the database offset and limit values for paginated queries.

    Takes a page number and items per page count and calculates the
    corresponding offset and limit values for database queries.

    Args:
        page_number: The requested page number (1-indexed)
        items_per_page: Number of items to display per page
        maximum_items_per_page: Maximum allowed items per page

    Returns:
        Dictionary with 'offset' and 'limit' keys
    """
    # Ensure page number is at least 1
    page_number = max(1, page_number)

    # Cap items per page at maximum
    items_per_page = min(items_per_page, maximum_items_per_page)

    # Calculate offset
    offset = (page_number - 1) * items_per_page

    return {
        "offset": offset,
        "limit": items_per_page,
        "page": page_number,
    }


def format_timestamp_for_display_in_user_timezone(
    timestamp: datetime,
    timezone_offset_hours: int = 0,
    display_format: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """
    Format a UTC timestamp for display in the user's local timezone.

    Converts a UTC datetime object to the user's timezone and formats
    it as a human-readable string.

    Args:
        timestamp: The UTC datetime to format
        timezone_offset_hours: The user's timezone offset from UTC
        display_format: The strftime format string to use

    Returns:
        Formatted datetime string in the user's timezone
    """
    # Apply timezone offset
    local_time = timestamp + timedelta(hours=timezone_offset_hours)

    # Format and return
    return local_time.strftime(display_format)
