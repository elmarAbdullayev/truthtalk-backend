from agora_token_builder import RtcTokenBuilder
from app.core.config import settings
import time
import random


def generate_agora_token(channel_name: str, uid: int = 0, role: int = 1) -> str:
    """
    Generate Agora RTC token

    Args:
        channel_name: Room channel name
        uid: User ID (0 for random)
        role: 1 = Publisher (can speak), 2 = Subscriber (listen only)
    """
    app_id = settings.AGORA_APP_ID
    app_certificate = settings.AGORA_APP_CERTIFICATE

    # Check if certificate exists
    if not app_certificate or app_certificate == "":
        raise ValueError("AGORA_APP_CERTIFICATE not configured in .env")

    # Token expires in 24 hours
    expiration_time_in_seconds = 3600 * 24
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    # Generate random UID if not provided
    if uid == 0:
        uid = random.randint(1, 999999)

    try:
        token = RtcTokenBuilder.buildTokenWithUid(
            app_id,
            app_certificate,
            channel_name,
            uid,
            role,
            privilege_expired_ts
        )
        return token
    except Exception as e:
        print(f"Agora token generation error: {e}")
        raise ValueError(f"Failed to generate Agora token: {str(e)}")