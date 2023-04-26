from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.settings.database import get_session
from model import Role, User, UserToRole
from routers.auth import get_current_active_user

def admin_role(session: Session = depends(get_session),
               current_user: User = depends(get_current_active_user)):
    # Get the role IDs for the 'role_admin' role
    admin_role_ids = []
    admin_roles = session.query(Role).filter(Role.name == 'ROLE_ADMIN').all()
    for admin_role in admin_roles:
        admin_role_ids.append(admin_role.id)
    # Check if the current user has any of the 'role_admin' roles
    user_to_roles = session.query(UserToRole).filter(
        UserToRole.user_id == current_user.id,
        UserToRole.role_id.in_(admin_role_ids)
    ).all()
    # If the user doesn't have any 'role_admin' roles, raise an exception
    if not user_to_roles:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return current_user

def moderator_role(session: Session = Depends(get_session),
                   current_user: User = Depends(get_current_active_user)):
    # Get all roles with name 'ROLE_MODERATOR'
    moderator_roles = session.query(Role).filter(Role.name == 'ROLE_MODERATOR').all()
    # Get IDs of moderator roles
    moderator_role_ids = [role.id for role in moderator_roles]
    # Check if current user has any of the moderator roles
    user_to_roles = session.query(UserToRole).\
                    filter(UserToRole.user_id == current_user.id).\
                    filter(UserToRole.role_id.in_(moderator_role_ids)).all()
    # If user has none of the moderator roles, raise 403 exception
    if not user_to_roles:
        raise HTTPException(403, "Unauthorized.")
    # Return current user if authorized
    return current_user

def user_role(session: Session = Depends(get_session),
              current_user: User = Depends(get_current_active_user)):
    # Define the allowed roles
    allowed_roles = ['ROLE_USER', 'ROLE_MODERATOR', 'ROLE_ADMIN']

    # Get the role IDs of the allowed roles
    roles = session.query(Role).filter(Role.name.in_(allowed_roles)).all()
    role_ids = [role.id for role in roles]

    # Check if the current user has any of the allowed roles
    user_roles = session.query(UserToRole).filter(
        UserToRole.user_id == current_user.id,
        UserToRole.role_id.in_(role_ids)).all()

    # If the user doesn't have any of the allowed roles, raise an exception
    if not user_roles:
        raise HTTPException(403, "Unauthorized.")

    # Otherwise, return the current user object
    return current_user
