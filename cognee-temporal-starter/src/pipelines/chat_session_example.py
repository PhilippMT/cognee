"""
Coding Agent Chat Session - Example Usage

This example demonstrates how to process coding agent chat sessions
with temporal awareness using Graphiti and Cognee.
"""

import asyncio
from datetime import datetime, timedelta
from cognee_temporal_starter.src.pipelines.chat_session_processor import process_coding_session


# Example chat history from a coding session
example_chat_history = [
    {
        "role": "user",
        "content": "I need to implement a user authentication system with JWT tokens. Can you help me design this?",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "message_id": "msg_001"
    },
    {
        "role": "assistant",
        "content": """I'll help you design a JWT-based authentication system. Let me break this down into components:

1. User Model (user.py) - Define user schema
2. Auth Service (auth_service.py) - Handle JWT generation and validation
3. Middleware (auth_middleware.py) - Protect routes
4. API Endpoints (auth_routes.py) - Login, register, refresh

Let's start with the User Model. I'll create a simple but secure implementation.""",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=-5)).isoformat(),
        "message_id": "msg_002"
    },
    {
        "role": "assistant",
        "content": """Here's the user model implementation:

```python
# models/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: str = Field(..., description="Unique user ID")
    email: EmailStr
    username: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    last_login: Optional[datetime] = None
```

I've used Pydantic for validation and included essential fields. The password will be hashed before storing.""",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=-10)).isoformat(),
        "message_id": "msg_003",
        "tool_calls": [
            {"tool": "create_file", "args": {"path": "models/user.py"}}
        ]
    },
    {
        "role": "user",
        "content": "Good start! But we should also add email verification and password reset functionality. Can you extend the model?",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=-15)).isoformat(),
        "message_id": "msg_004",
        "parent_message_id": "msg_003"
    },
    {
        "role": "assistant",
        "content": """Excellent point! I'll extend the user model with email verification and password reset capabilities.

I'll add:
- email_verified: bool
- verification_token: Optional[str]
- verification_token_expires: Optional[datetime]
- reset_password_token: Optional[str]
- reset_password_token_expires: Optional[datetime]

Here's the updated model:""",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=-17)).isoformat(),
        "message_id": "msg_005"
    },
    {
        "role": "assistant",
        "content": """```python
# models/user.py (updated)
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: str = Field(..., description="Unique user ID")
    email: EmailStr
    username: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    last_login: Optional[datetime] = None
    
    # Email verification
    email_verified: bool = False
    verification_token: Optional[str] = None
    verification_token_expires: Optional[datetime] = None
    
    # Password reset
    reset_password_token: Optional[str] = None
    reset_password_token_expires: Optional[datetime] = None
```

Now let's implement the JWT service.""",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=-20)).isoformat(),
        "message_id": "msg_006",
        "tool_calls": [
            {"tool": "edit_file", "args": {"path": "models/user.py"}}
        ]
    },
    {
        "role": "user",
        "content": "Perfect! Now let's implement the JWT service with token refresh functionality.",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-55)).isoformat(),
        "message_id": "msg_007"
    },
    {
        "role": "assistant",
        "content": """I'll implement a comprehensive JWT service with access and refresh tokens.

Decision: I'll use PyJWT library for token generation and validation. We'll have:
- Short-lived access tokens (15 minutes)
- Long-lived refresh tokens (7 days)
- Token rotation on refresh

Creating auth_service.py...""",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-50)).isoformat(),
        "message_id": "msg_008"
    },
    {
        "role": "assistant",
        "content": """```python
# services/auth_service.py
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.hash import bcrypt
import secrets

class AuthService:
    SECRET_KEY = "your-secret-key-here"  # Should be in environment
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.verify(password, password_hash)
    
    @staticmethod
    def create_access_token(user_id: str, email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(days=AuthService.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "user_id": user_id,
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")
```

This implementation provides secure token management with proper expiration.""",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-45)).isoformat(),
        "message_id": "msg_009",
        "tool_calls": [
            {"tool": "create_file", "args": {"path": "services/auth_service.py"}}
        ]
    },
    {
        "role": "tool",
        "content": "File created successfully: services/auth_service.py",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-44)).isoformat(),
        "message_id": "msg_010"
    },
    {
        "role": "user",
        "content": "Great! I noticed we're storing the secret key in code. We should move that to environment variables for security.",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-40)).isoformat(),
        "message_id": "msg_011"
    },
    {
        "role": "assistant",
        "content": """Absolutely correct! That's a security issue. I'll refactor to use environment variables.

This is a critical security fix - hardcoded secrets are a major vulnerability. I'll update the code to use os.getenv() for the secret key.""",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-38)).isoformat(),
        "message_id": "msg_012"
    },
    {
        "role": "assistant",
        "content": """```python
# services/auth_service.py (updated)
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.hash import bcrypt

class AuthService:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable must be set")
    
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # ... rest of the implementation
```

I've also made the token expiration times configurable via environment variables with sensible defaults.""",
        "timestamp": (datetime.now() - timedelta(hours=1, minutes=-35)).isoformat(),
        "message_id": "msg_013",
        "tool_calls": [
            {"tool": "edit_file", "args": {"path": "services/auth_service.py"}}
        ]
    },
    {
        "role": "user",
        "content": "Perfect! The authentication system looks complete. Let's create a summary of what we've built.",
        "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "message_id": "msg_014"
    },
    {
        "role": "assistant",
        "content": """# JWT Authentication System - Implementation Summary

## Components Implemented:

### 1. User Model (models/user.py)
- User schema with Pydantic validation
- Email verification support
- Password reset functionality
- Secure password hashing

### 2. Auth Service (services/auth_service.py)
- JWT token generation (access + refresh)
- Password hashing with bcrypt
- Environment-based configuration
- Token expiration management

## Security Features:
✅ Password hashing (bcrypt)
✅ JWT tokens with expiration
✅ Token refresh mechanism
✅ Environment-based secrets
✅ Email verification support
✅ Password reset capability

## Next Steps:
- Implement auth middleware for route protection
- Create API endpoints (login, register, refresh, verify email)
- Add rate limiting
- Implement token revocation (blacklist)
- Add 2FA support (optional)

The system is now ready for the middleware and API endpoint implementation!""",
        "timestamp": (datetime.now() - timedelta(minutes=28)).isoformat(),
        "message_id": "msg_015"
    }
]


async def main():
    """
    Main example function demonstrating chat session processing.
    """
    print("=" * 80)
    print("Coding Agent Chat Session Processing Example")
    print("=" * 80)
    print()
    
    # Process the chat session
    results = await process_coding_session(
        chat_history=example_chat_history,
        session_id="auth_system_implementation_001",
        use_graphiti=True,
        extract_deep_facts=True,
        preserve_raw_data=True
    )
    
    print()
    print("=" * 80)
    print("Processing Results:")
    print("=" * 80)
    for key, value in results.items():
        print(f"{key}: {value}")
    
    print()
    print("=" * 80)
    print("Example Complete!")
    print("=" * 80)
    print()
    print("What happened:")
    print("1. ✅ Parsed and normalized 15 messages from coding session")
    print("2. ✅ Created Graphiti episodes with temporal context")
    print("3. ✅ Extracted events using temporal_cognify")
    print("4. ✅ Mined development facts (code changes, bug fixes, features)")
    print("5. ✅ Identified agent decisions and their rationales")
    print("6. ✅ Tracked code entities (files, functions) and their evolution")
    print("7. ✅ Built session metadata and timeline")
    print("8. ✅ Indexed all artifacts for efficient retrieval")
    print()
    print("Next steps:")
    print("- Query the temporal graph for development insights")
    print("- Search for specific facts, decisions, or code entities")
    print("- Build timelines showing development progression")
    print("- Find patterns across multiple sessions")
    print("- Generate development reports from extracted data")


if __name__ == "__main__":
    asyncio.run(main())
