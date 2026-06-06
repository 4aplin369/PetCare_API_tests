import allure
import api

import pytest

from src import data as d

from helpers import helpers as h


class TestOwnerRegister:
    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Создание владельца")
    @allure.title("Регистрация владельца")
    def test_owner_register(self):
        name, email, phone = h.get_owner_register_data()
        r = api.owner_register(name, email, phone)
        h.get_id_and_delete_owner(r)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 201

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CREATE_RESPONSE_TEXT in r.text

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Создание владельца")
    @allure.title("Регистрация владельца который уже существует")
    def test_owner_register_already_exist(self):
        name, email, phone = h.get_owner_register_data()
        r = api.owner_register(name, email, phone)
        r = api.owner_register(name, email, phone)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 409

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CREATE_ALREADY_EXIST_TEXT in r.text

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Создание владельца")
    @allure.title("Регистрация владельца с неполными данными")
    @pytest.mark.parametrize(
        "no_data",
        ["name", "email", "phone"],
        ids=["without_name", "without_email", "without_phone"],
    )
    def test_owner_register_no_data(self, no_data):
        name, email, phone = h.get_owner_register_data()
        payload = {"name": name, "email": email, "phone": phone}
        payload.pop(no_data)
        r = api.owner_register_with_custom_payload(payload=payload)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 422

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CREATE_NO_DATA_TEXT in r.text

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Создание владельца")
    @allure.title("Регистрация владельца с пустыми данными")
    @pytest.mark.parametrize(
        "empty_data",
        ["name", "email", "phone"],
        ids=["empty_name", "empty_email", "empty_phone"],
    )
    def test_owner_register_empty_data(self, empty_data):
        name, email, phone = h.get_owner_register_data()
        payload = {"name": name, "email": email, "phone": phone}
        payload[empty_data] = ""
        r = api.owner_register_with_custom_payload(payload=payload)

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 422

        if empty_data == phone:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_DATA_TEXT in r.text

        if empty_data == email:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_EMAIL_OR_NAME_TEXT in r.text

        if empty_data == name:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_EMAIL_OR_NAME_TEXT in r.text
