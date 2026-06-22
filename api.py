import requests
import src.data as d

from allure import step


@step("Проверка доступности сайта")
def health_check():
    response = requests.get(d.HEALTH_CHECK_URL)
    return response


@step("Регистрация владельца")
def owner_register(name, email, phone):
    payload = {"name": name, "email": email, "phone": phone}

    response = requests.post(
        d.OWNER_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    return response


@step("Регистрация владельца")
def owner_register_with_custom_payload(payload):
    response = requests.post(
        d.OWNER_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    return response


@step("Получение списка владельцев")
def get_owners():
    response = requests.get(d.OWNER_URL)
    return response


@step("Удаление владельца")
def owner_delete(owner_id):
    response = requests.delete(
        f"{d.OWNER_URL}/{owner_id}", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200


@step("Изменение данных владельца")
def owner_change_data_with_custom_payload(owner_id, owner_key, owner_value):
    payload = {owner_key: owner_value}
    response = requests.patch(
        f"{d.OWNER_URL}/{owner_id}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return response


@step("Регистрация питомца")
def pet_register(age, breed, name, notes, owner_id, species):
    payload = {
        "age": age,
        "breed": breed,
        "name": name,
        "notes": notes,
        "owner_id": owner_id,
        "species": species,
    }

    response = requests.post(
        d.PET_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    return response


@step("Регистрация питомца")
def pet_register_with_custom_payload(payload):
    response = requests.post(
        d.PET_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    return response


@step("Удаление питомца")
def pet_delete(pet_id):
    response = requests.delete(
        f"{d.PET_URL}/{pet_id}", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200


@step("Получение списка питомцев")
def get_pets():
    response = requests.get(d.PET_URL)
    return response

    assert response.status_code == 200


@step("Получение списка питомцев С сортировкой по типу питомца")
def get_pets_species_sorting(species):
    response = requests.get(f"{d.PET_URL}?species={species}")
    return response
    assert response.status_code == 200


@step("Получение списка питомцев С сортировкой по слову")
def get_pets_search_sorting(word):
    response = requests.get(f"{d.PET_URL}?search={word}")
    return response
    assert response.status_code == 200


@step("Создание записи на прием")
def add_appoinment(pet_id, reason, starts_at, vet_id):
    payload = {
        "pet_id": pet_id,
        "reason": reason,
        "starts_at": starts_at,
        "vet_id": vet_id,
    }
    response = requests.post(
        d.APPOINMENT_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    return response


@step("Отмена записи к врачу")
def appoinment_delete(appoinment_id):
    response = requests.delete(
        f"{d.APPOINMENT_URL}/{appoinment_id}",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200


@step("Удаление записи для очистки тестовых данных")
def appoinment_hard_delete(appoinment_id):
    response = requests.delete(
        f"{d.APPOINMENT_DEV_URL}/{appoinment_id}",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    return response

@step("Добавление записи")
def add_appoinment_with_custom_payload(payload):
    response = requests.post(
        d.APPOINTMENT_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return response