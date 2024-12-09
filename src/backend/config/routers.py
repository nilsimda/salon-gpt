from enum import StrEnum

from fastapi import Depends

from backend.database_models import get_session
from backend.services.auth.request_validators import (
    ScimAuthValidation,
    validate_authorization,
)
from backend.services.request_validators import (
    validate_chat_request,
    validate_organization_header,
    validate_user_header,
)


# Important! Any new routers must have a corresponding RouterName entry and Router dependencies
# mapping below. Make sure they use the correct ones depending on whether authentication is enabled or not.
class RouterName(StrEnum):
    AUTH = "auth"
    CHAT = "chat"
    SEARCH = "search"
    TRANSCRIBE = "transcribe"
    CONVERSATION = "conversation"
    USER = "user"
    AGENT = "agent"
    DEFAULT_AGENT = "default_agent"
    SNAPSHOT = "snapshot"
    STUDY = "study"
    SCIM = "scim"


# Router dependency mappings
ROUTER_DEPENDENCIES = {
    RouterName.AUTH: {
        "default": [
            Depends(get_session),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_organization_header),
        ],
    },
    RouterName.CHAT: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_chat_request),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_chat_request),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.SEARCH: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_chat_request),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_chat_request),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.TRANSCRIBE: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_chat_request),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_chat_request),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.CONVERSATION: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.USER: {
        "default": [
            Depends(get_session),
            Depends(validate_organization_header),
        ],
        "auth": [
            # TODO: Remove auth only for create user endpoint
            Depends(get_session),
            Depends(validate_organization_header),
        ],
    },
    RouterName.AGENT: {
        "default": [
            Depends(get_session),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.DEFAULT_AGENT: {
        "default": [
            Depends(get_session),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.SNAPSHOT: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.STUDY: {
        "default": [
            Depends(get_session),
            Depends(validate_user_header),
            Depends(validate_organization_header),
        ],
        "auth": [
            Depends(get_session),
            Depends(validate_authorization),
            Depends(validate_organization_header),
        ],
    },
    RouterName.SCIM: {
        "default": [
            Depends(get_session),
            Depends(ScimAuthValidation()),
        ],
        "auth": [
            Depends(ScimAuthValidation()),
        ],
    },
}
