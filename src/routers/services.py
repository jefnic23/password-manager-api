from fastapi import APIRouter, HTTPException, status

from src.dependencies import CURRENT_USER_DEPENDENCY, SERVICES_SERVICE_DEPENDENCY
from src.schemas.create_service_request import CreateServiceRequest

router = APIRouter()


@router.get("/services")
async def get_all_services(
    current_user: CURRENT_USER_DEPENDENCY,
    services_service: SERVICES_SERVICE_DEPENDENCY,
) -> list[str]:
    return await services_service.get_all(user_id=current_user.id)


@router.post("/services", status_code=status.HTTP_201_CREATED)
async def add_service(
    current_user: CURRENT_USER_DEPENDENCY,
    services_service: SERVICES_SERVICE_DEPENDENCY,
    body: CreateServiceRequest,
) -> str:
    new_password = services_service.generate_password()
    encrypted_password = services_service.encrypt_password(new_password)
    await services_service.add(
        user_id=current_user.id, name=body.name, password=encrypted_password
    )
    return new_password


@router.get("/services/{name}")
async def get_service(
    current_user: CURRENT_USER_DEPENDENCY,
    services_service: SERVICES_SERVICE_DEPENDENCY,
    name: str,
) -> str:
    encrypted_password = await services_service.get(user_id=current_user.id, name=name)
    if not encrypted_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password not found",
        )
    return services_service.decrypt_password(encrypted_password)


@router.delete("/services/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    current_user: CURRENT_USER_DEPENDENCY,
    services_service: SERVICES_SERVICE_DEPENDENCY,
    name: str,
) -> None:
    deleted = await services_service.delete(user_id=current_user.id, name=name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password not found",
        )


@router.put("/services/{name}")
async def update_service(
    current_user: CURRENT_USER_DEPENDENCY,
    services_service: SERVICES_SERVICE_DEPENDENCY,
    name: str,
) -> str:
    new_password = services_service.generate_password()
    encrypted_password = services_service.encrypt_password(new_password)
    await services_service.update(
        user_id=current_user.id, name=name, password=encrypted_password
    )
    return new_password
