from fastapi import HTTPException, status


def require_role(user, role: str):
    """
    Require a single role.
    """

    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied.",
        )

    return user


def require_any_role(user, roles: list[str]):
    """
    Require one of multiple roles.
    """

    if user.role not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied.",
        )

    return user