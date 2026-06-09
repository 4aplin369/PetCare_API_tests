import allure
import api

import pytest

from src import data as d

from helpers import helpers as h


class TestPetRegister:
    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Создание питомца")
    @allure.title("Регистрация питомца")
    def test_pet_register(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert pet_r.status_code == 201

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CREATE_RESPONSE_TEXT in pet_r.text

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Создание питомца")
    @allure.title("Регистрация питомца, который уже существует")
    def test_owner_register_already_exist(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)
        pet_r_double = api.pet_register(age, breed, name, notes, owner_id, species)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert pet_r_double.status_code == 409

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.PET_ALREADY_EXIST_TEXT in pet_r_double.text

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Создание питомца")
    @allure.title("Регистрация питомца с несуществующим владельцем")
    def test_pet_register_owner_not_exist(self):
        owner_id = h.generate_random_id()

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(owner_id)
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert pet_r.status_code == 404

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_NOT_FOUND_TEXT in pet_r.text

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Создание питомца")
    @allure.title("Регистрация питомца с неполными данными")
    @pytest.mark.parametrize(
        "no_data",
        ["age", "breed", "name", "notes", "owner_id", "species"],
        ids=[
            "without_age",
            "without_breed",
            "without_name",
            "without_notes",
            "without_owner_id",
            "without species",
        ],
    )
    def test_pet_register_no_data(self, no_data):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )

        payload = {
            "age": age,
            "breed": breed,
            "name": name,
            "notes": notes,
            "owner_id": owner_id,
            "species": species,
        }
        payload.pop(no_data)
        pet_r = api.pet_register_with_custom_payload(payload=payload)

        if no_data == "notes":
            with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
                assert pet_r.status_code == 201

            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_RESPONSE_TEXT in pet_r.text

            h.get_id_and_delete_pet(pet_r)

        else:
            with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
                assert pet_r.status_code == 422

            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_NO_DATA_TEXT in pet_r.text

        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Создание питомца")
    @allure.title("Регистрация питомца с пустыми данными")
    @pytest.mark.parametrize(
        "empty_data",
        ["age", "breed", "name", "notes", "owner_id", "species"],
        ids=[
            "empty_age",
            "empty_breed",
            "empty_name",
            "empty_notes",
            "empty_owner_id",
            "empty species",
        ],
    )
    def test_pet_register_empty_data(self, empty_data):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )

        payload = {
            "age": age,
            "breed": breed,
            "name": name,
            "notes": notes,
            "owner_id": owner_id,
            "species": species,
        }
        payload[empty_data] = ""
        pet_r = api.pet_register_with_custom_payload(payload=payload)

        if empty_data in ("notes"):
            with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
                assert pet_r.status_code == 201

            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_RESPONSE_TEXT in pet_r.text

            h.get_id_and_delete_pet(pet_r)

        elif empty_data in ("species", "breed", "name"):
            with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
                assert pet_r.status_code == 422

            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.PET_NO_TYPE_TEXT in pet_r.text

        else:
            with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
                assert pet_r.status_code == 422

            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.PET_NO_AGE_TEXT in pet_r.text

        h.get_id_and_delete_owner(r)
