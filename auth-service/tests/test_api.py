import pytest
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_register_success(client, sample_user_data):
    response = await client.post("/auth/register", json=sample_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, sample_user_data):
    await client.post("/auth/register", json=sample_user_data)
    response = await client.post("/auth/register", json=sample_user_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client, sample_user_data):
    await client.post("/auth/register", json=sample_user_data)
    response = await client.post(
        "/auth/login",
        data={
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client, sample_user_data):
    await client.post("/auth/register", json=sample_user_data)
    response = await client.post(
        "/auth/login",
        data={
            "username": sample_user_data["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post(
        "/auth/login",
        data={
            "username": "nonexistent@email.com",
            "password": "123456"
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_valid_token(client, sample_user_data):
    await client.post("/auth/register", json=sample_user_data)
    login_response = await client.post(
        "/auth/login",
        data={
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]


@pytest.mark.asyncio
async def test_me_without_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token(client):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
