import requests


base_url = "http://0.0.0.0:5000/api/"
client = requests.Session()


def test_get_all_users() -> None:
    response = client.get(f"{base_url}users/")
    users = response.json()

    assert response.status_code == 200
    assert type(users) == list
    assert len(users) == 100


def test_get_single_user() -> None:
    response1 = client.get(f"{base_url}users/")
    users = response1.json()
    assert response1.status_code == 200
    assert type(users) == list
    assert len(users) == 100

    response = client.get(f"{base_url}users/{users[0]['id']}/")
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_single_user_incorrect() -> None:
    response1 = client.get(f"{base_url}users/")
    users = response1.json()
    assert response1.status_code == 200
    assert type(users) == list
    assert len(users) == 100

    response2 = client.get(f"{base_url}users/{users[-1]['id'] + 1}/")
    assert response2.status_code == 404
    assert response2.json()["detail"] == "Object does not exist"
