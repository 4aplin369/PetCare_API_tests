import allure
import api
from src import data as d


class TestHealthCheck:
    @allure.epic("PetCare")
    @allure.feature("Сайт")
    @allure.story("Проверки здоровья")
    @allure.title("Проверка доступности сайта")
    def test_health_check(self):
        r = api.health_check()

        with allure.step(d.ALLURE_RESULT_CORRECT_TEXT):
            assert d.HEALTH_CHECK_RESPONSE_TEXT == r.text
        with allure.step(d.ALLURE_RESULT_CORRECT_CODE):
            assert r.status_code == 200
