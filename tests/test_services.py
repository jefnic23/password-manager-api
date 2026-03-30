import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from src.models.service import Service

from .conftest import USER_ONE, USER_TWO


class TestDeleteService:
    async def test_delete_existing_service_returns_204(self, client, session):
        service = Service(name="gmail", password="encrypted", user_id=USER_ONE.id)
        session.add(service)
        await session.commit()

        response = await client.delete("/services/gmail")

        assert response.status_code == 204

    async def test_deleted_service_is_gone(self, client, session):
        service = Service(name="gmail", password="encrypted", user_id=USER_ONE.id)
        session.add(service)
        await session.commit()

        await client.delete("/services/gmail")
        response = await client.get("/services/gmail")

        assert response.status_code == 404

    async def test_delete_nonexistent_service_returns_404(self, client):
        response = await client.delete("/services/nonexistent")

        assert response.status_code == 404

    async def test_delete_does_not_affect_other_users_service(self, client, session):
        # USER_TWO owns a service named "gmail"
        service = Service(name="gmail", password="encrypted", user_id=USER_TWO.id)
        session.add(service)
        await session.commit()

        # USER_ONE tries to delete it — should be 404
        response = await client.delete("/services/gmail")
        assert response.status_code == 404

        # The service should still exist for USER_TWO
        result = await session.exec(
            select(Service).where(Service.user_id == USER_TWO.id).where(Service.name == "gmail")
        )
        assert result.first() is not None


class TestUniqueConstraintPerUser:
    async def test_two_users_can_share_a_service_name(self, services_svc, session):
        await services_svc.add(user_id=USER_ONE.id, name="gmail", password="enc1")
        await services_svc.add(user_id=USER_TWO.id, name="gmail", password="enc2")

        result = await session.exec(select(Service).where(Service.name == "gmail"))
        services = result.all()

        assert len(services) == 2
        assert {s.user_id for s in services} == {USER_ONE.id, USER_TWO.id}

    async def test_same_user_cannot_add_duplicate_service_name(self, services_svc):
        await services_svc.add(user_id=USER_ONE.id, name="gmail", password="enc1")

        with pytest.raises(IntegrityError):
            await services_svc.add(user_id=USER_ONE.id, name="gmail", password="enc2")
