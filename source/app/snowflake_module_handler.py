from __future__ import annotations
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


class SnowflakeHandler:
    """Handles _snowflake imports and mocking for local development."""

    @staticmethod
    def get_snowflake_module():
        try:
            # this import only exists on snowflake
            import _snowflake

            return _snowflake
        except ImportError:
            # Mock _snowflake for local development
            class MockSnowflake:
                @staticmethod
                def get_username_password(key):
                    return type(
                        "Credentials",
                        (object,),
                        {
                            "username": os.getenv("USERNAME"),
                            "password": os.getenv("PASSWORD"),
                        },
                    )

            return MockSnowflake()
