import allure
import api

import pytest

from src import data as d

from helpers import helpers as h


class TestOwnerChangeData:
    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Изменение владельца")
    @allure.title("Изменение данных владельца")
    @pytest.mark.parametrize(
        "change_key, change_value",
        [
            ("name", h.get_fake_fullname),
            ("email", h.get_fake_email),
            ("phone", h.get_fake_phone),
        ],
        ids=["name", "email", "phone"],
    )
    def test_owner_change(self, change_key, change_value):
        name, email, phone = h.get_owner_register_data()
        r_for_delete = api.owner_register(name, email, phone)

        new_value = change_value()

        r_json = r_for_delete.json()
        owner_id = r_json["id"]

        r = api.owner_change_data_with_custom_payload(
            owner_id=owner_id, owner_key=change_key, owner_value=new_value
        )
        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 200

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert new_value in r.text

        h.get_id_and_delete_owner(r_for_delete)

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Изменение владельца")
    @allure.title("Изменение данных владельца на пустые")
    @pytest.mark.parametrize(
        "change_key, change_value",
        [
            ("name", ""),
            ("email", ""),
            ("phone", ""),
        ],
        ids=["name", "email", "phone"],
    )
    def test_owner_change_empty_data(self, change_key, change_value):
        name, email, phone = h.get_owner_register_data()
        r_for_delete = api.owner_register(name, email, phone)

        r_json = r_for_delete.json()
        owner_id = r_json["id"]

        r = api.owner_change_data_with_custom_payload(
            owner_id=owner_id, owner_key=change_key, owner_value=change_value
        )
        if change_key == phone:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_DATA_TEXT in r.text

        if change_key == email:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_EMAIL_OR_NAME_TEXT in r.text

        if change_key == name:
            with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
                assert d.OWNER_CREATE_EMPTY_EMAIL_OR_NAME_TEXT in r.text

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 422
        h.get_id_and_delete_owner(r_for_delete)

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Изменение владельца")
    @allure.title("Изменение данных валидация не пройдена")
    def test_owner_change_validation_error(self):
        r = api.owner_change_data_with_custom_payload(
            owner_id=h.generate_random_string(2),
            owner_key=h.generate_random_string(5),
            owner_value=h.generate_random_string(5),
        )
        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 422
        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CHANGE_VALIDATION_ERROR_TEXT in r.text

    @allure.epic("PetCare")
    @allure.feature("Администрирование владельцев")
    @allure.story("Изменение владельца")
    @allure.title("Изменение данных владелец не найден")
    def test_owner_change_id_not_found(self):
        r = api.owner_change_data_with_custom_payload(
            owner_id=h.generate_random_id(),
            owner_key="email",
            owner_value=h.get_fake_email(),
        )
        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 404
        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.OWNER_CHANGE_OWNER_NOT_FOUND in r.text
