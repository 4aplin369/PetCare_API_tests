import allure
import api

from helpers import helpers as h


class TestPetRegister:
    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Список питомцев")
    @allure.title("Созданный питомец появляется в списке")
    def test_get_pets(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        r_pets = api.get_pets()
        created_pet_json = r_pets.json()

        assert created_pet_json[-1]["name"] == name
        assert created_pet_json[-1]["species"] == species
        assert created_pet_json[-1]["breed"] == breed
        assert created_pet_json[-1]["age"] == age
        assert created_pet_json[-1]["owner_id"] == owner_id
        assert created_pet_json[-1]["notes"] == notes

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Список питомцев")
    @allure.title("Сортировка в списке питомцев по типу питомца")
    def test_get_pets_species_sorting(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        r_pets = api.get_pets_species_sorting(species)
        created_pet_json = r_pets.json()

        for pet in created_pet_json:
            assert pet["species"] == species

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Список питомцев")
    @allure.title("Сортировка в списке питомцев по имени")
    def test_get_pets_name_sorting(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        r_pets = api.get_pets_search_sorting(name)
        created_pet_json = r_pets.json()

        for pet in created_pet_json:
            assert pet["name"] == name

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Список питомцев")
    @allure.title("Сортировка в списке питомцев по породе")
    def test_get_pets_breed_sorting(self):
        owner_name, email, phone = h.get_owner_register_data()
        r = api.owner_register(owner_name, email, phone)

        age, breed, name, notes, owner_id, species = h.get_pet_register_data(
            owner_id=h.get_id_owner(r)
        )
        pet_r = api.pet_register(age, breed, name, notes, owner_id, species)

        r_pets = api.get_pets_search_sorting(breed)
        created_pet_json = r_pets.json()

        for pet in created_pet_json:
            assert pet["breed"] == breed

        h.get_id_and_delete_pet(pet_r)
        h.get_id_and_delete_owner(r)

    @allure.epic("PetCare")
    @allure.feature("Администрирование питомцев")
    @allure.story("Список питомцев")
    @allure.title("Сортировка в списке питомцев пустой результат")
    def test_get_pets_search_empty_result(self):
        r_pets = api.get_pets_search_sorting(h.generate_random_string(11))
        pets_list = r_pets.json()
        assert pets_list == []
