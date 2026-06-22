import allure
import api

import pytest

from src import data as d

from helpers import helpers as h


class TestAddAppoinment:
    @allure.epic("PetCare")
    @allure.feature("Администрирование записей на прием")
    @allure.story("Добавление записи")
    @allure.title("Добавление записи корректно")
    def test_add_appoinment(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)
        pet_r_json = pet_r.json()
        pet_id, reason, starts_at, vet_id = (
            pet_r_json["id"],
            h.generate_random_string(20),
            h.generate_starts_at(),
            1,
        )

        response = api.add_appoinment(pet_id, reason, starts_at, vet_id)

        response_json = response.json()

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert response.status_code == 201

        assert response_json["pet_id"] == pet_id
        assert response_json["vet_id"] == vet_id
        assert response_json["starts_at"] == starts_at
        assert response_json["reason"] == reason
        assert response_json["status"] == "scheduled"
        assert "id" in response_json

        api.appoinment_hard_delete(response.json()["id"])
        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование записей на прием")
    @allure.story("Добавление записи")
    @allure.title("Добавление записи: питомец или врач не найден")
    @pytest.mark.parametrize(
        "pet_id_override, vet_id_override, expected_error",
        [
            (999999, 1, "Pet not found"),
            (None, 999999, "Vet not found"),
        ],
        ids=["pet_not_found", "vet_not_found"],
    )
    def test_add_appoinment_pet_or_vet_not_found(
        self,
        pet_id_override,
        vet_id_override,
        expected_error,
    ):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)
        pet_r_json = pet_r.json()

        pet_id = pet_id_override or pet_r_json["id"]
        vet_id = vet_id_override

        reason = h.generate_random_string(20)
        starts_at = h.generate_starts_at()

        response = api.add_appoinment(pet_id, reason, starts_at, vet_id)
        response_json = response.json()

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert response.status_code == 404

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert response_json["detail"] == expected_error

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование записей на прием")
    @allure.story("Добавление записи")
    @allure.title("Добавление записи, врач уже занят на это время")
    def test_add_appoinment_vet_slot_conflict(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)
        pet_r_json = pet_r.json()

        pet_id, reason, starts_at, vet_id = (
            pet_r_json["id"],
            h.generate_random_string(20),
            h.generate_starts_at(),
            1,
        )

        r_to_delete = api.add_appoinment(pet_id, reason, starts_at, vet_id)
        response = api.add_appoinment(pet_id, reason, starts_at, vet_id)

        response_json = response.json()

        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert response.status_code == 409

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert response_json["detail"] == d.VET_IS_BUSY_TEXT

        api.appoinment_hard_delete(r_to_delete.json()["id"])
        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)
