"""
Core configuration constants.
"""

# API Metadata
API_TITLE = "Job Application API"
API_VERSION = "2.0.0"
API_DESCRIPTION = "A REST API for managing job applications with user authentication"

# Application Status Enums
APPLICATION_STATUS_PENDING = "pending"
APPLICATION_STATUS_REVIEWING = "reviewing"
APPLICATION_STATUS_ACCEPTED = "accepted"
APPLICATION_STATUS_REJECTED = "rejected"

APPLICATION_STATUSES = [
    APPLICATION_STATUS_PENDING,
    APPLICATION_STATUS_REVIEWING,
    APPLICATION_STATUS_ACCEPTED,
    APPLICATION_STATUS_REJECTED,
]

# Token Types
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# HTTP Status Messages
SUCCESS_MESSAGE = "Operation completed successfully"
ERROR_MESSAGE = "An error occurred"
