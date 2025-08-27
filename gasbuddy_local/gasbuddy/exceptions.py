"""Exceptions for the py-gasbuddy library."""

class GasBuddyError(Exception):
    """Base exception for GasBuddy errors."""

class APIError(GasBuddyError):
    """Raised when the GasBuddy API returns an error."""

class CSRFTokenMissing(GasBuddyError):
    """Raised when the CSRF token cannot be retrieved."""

class LibraryError(GasBuddyError):
    """Raised when there's an error in the library."""

class MissingSearchData(GasBuddyError):
    """Raised when location search data is missing."""
