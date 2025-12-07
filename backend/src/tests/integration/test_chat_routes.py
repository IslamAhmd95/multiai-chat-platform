import pytest

from src.models.chat_history import ChatHistory
from src.core.enums import AIModels


@pytest.fixture
def authenticated_user(client, test_db):
    from src.models.user import User
    from src.core.hashing import hash_password

    user = User(
        email="chatuser@example.com",
        username="chatuser",
        name="Chat User",
        password=hash_password("password123")
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    response = client.post("/auth/login", json={
        "login": "chatuser@example.com",
        "password": "password123"
    })
    token = response.json()["access_token"]
    
    return user, token


def test_get_platforms_returns_all_models(client):
    
    response = client.get("/ai/platforms")
    
    assert response.status_code == 200
    data = response.json()
    assert "platforms" in data
    assert isinstance(data["platforms"], list)
    assert len(data["platforms"]) > 0


def test_get_platforms_includes_gemini(client):
    
    response = client.get("/ai/platforms")
    
    platforms = response.json()["platforms"]
    assert AIModels.GEMINI.value in platforms


def test_get_platforms_includes_groq(client):
    
    response = client.get("/ai/platforms")
    
    platforms = response.json()["platforms"]
    assert AIModels.GROQ.value in platforms


def test_get_chat_history_requires_authentication(client):
    
    response = client.get(f"/ai/chat-history?model_name={AIModels.GEMINI.value}")
    
    assert response.status_code == 401


def test_get_chat_history_returns_user_chats(client, test_db, authenticated_user):
    user, access_token = authenticated_user

    chat1 = ChatHistory(
        user_id=user.id,
        prompt="Hello",
        response="Hi there!",
        model_name=AIModels.GEMINI
    )
    chat2 = ChatHistory(
        user_id=user.id,
        prompt="How are you?",
        response="I'm doing well!",
        model_name=AIModels.GEMINI
    )
    test_db.add(chat1)
    test_db.add(chat2)
    test_db.commit()

    response = client.get(f'/ai/chat-history?model_name={AIModels.GEMINI.value}',
                           headers={"Authorization": f"Bearer {access_token}"}
                        )
    
    assert response.status_code == 200
    data = response.json()
    assert "chat" in data
    assert len(data["chat"]) == 2


def test_get_chat_history_filters_by_model(client, test_db, authenticated_user):
    
    user, token = authenticated_user
    
    gemini_chat = ChatHistory(
        user_id=user.id,
        prompt="Gemini prompt",
        response="Gemini response",
        model_name=AIModels.GEMINI
    )
    groq_chat = ChatHistory(
        user_id=user.id,
        prompt="Groq prompt",
        response="Groq response",
        model_name=AIModels.GROQ
    )
    test_db.add(gemini_chat)
    test_db.add(groq_chat)
    test_db.commit()
    
    response = client.get(
        f"/ai/chat-history?model_name={AIModels.GEMINI.value}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    data = response.json()
    print(data['chat'])
    assert len(data["chat"]) == 1
    assert data["chat"][0]["model_name"] == AIModels.GEMINI.value


def test_get_chat_history_returns_empty_when_no_chats(client, authenticated_user):
    
    user, token = authenticated_user
    
    response = client.get(
        f"/ai/chat-history?model_name={AIModels.GEMINI.value}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    data = response.json()
    assert data["chat"] == []


def test_get_chat_history_only_returns_own_chats(client, test_db, authenticated_user):
    from src.models.user import User
    from src.core.hashing import hash_password
    
    user, token = authenticated_user
    
    other_user = User(
        email="other@example.com",
        username="otheruser",
        name="Other User",
        password=hash_password("password123")
    )
    test_db.add(other_user)
    test_db.commit()
    test_db.refresh(other_user)
    
    other_chat = ChatHistory(
        user_id=other_user.id,
        prompt="Other user's chat",
        response="Response",
        model_name=AIModels.GEMINI
    )
    test_db.add(other_chat)
    test_db.commit()
    
    response = client.get(
        f"/ai/chat-history?model_name={AIModels.GEMINI.value}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    data = response.json()
    assert len(data["chat"]) == 0