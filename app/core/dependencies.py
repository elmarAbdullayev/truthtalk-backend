from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Optional User (für Guest Access)
def get_current_user_optional(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User | None:
    try:
        return get_current_user(token, db)
    except:
        return None

    # ✅ Admin Dependency - Only Admins can access
def get_admin_user(
    current_user: User = Depends(get_current_user)
    ) -> User:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )
        return current_user