GENERAL_URL = "http://127.0.0.1:8000/api/"
HEALTH_CHECK_URL = "http://127.0.0.1:8000/health"
OWNER_URL = GENERAL_URL + "owners"
PET_URL = GENERAL_URL + "pets"
APPOINMENT_URL = GENERAL_URL + "appointments"
APPOINMENT_DEV_URL = GENERAL_URL + "dev/appointments"

ALLURE_RESULT_CORRECT_TEXT = "Проверка корректности респонса"
ALLURE_RESULT_CORRECT_CODE = "Проверка кода ответа"
HEALTH_CHECK_RESPONSE_TEXT = '{"status":"ok","service":"petcare-portal"}'
OWNER_CREATE_RESPONSE_TEXT = '{"id":'
OWNER_CREATE_NO_DATA_TEXT = "Field required"
OWNER_CREATE_ALREADY_EXIST_TEXT = "Owner with this email already exists"
OWNER_CREATE_EMPTY_PHONE_TEXT = "String should have at least 7 characters"
OWNER_CREATE_EMPTY_EMAIL_OR_NAME_TEXT = "An email address must have an @-sign."
OWNER_CREATE_EMPTY_NAME_TEXT = "String should have at least 2 characters"
OWNER_CHANGE_VALIDATION_ERROR_TEXT = (
    "Input should be a valid integer, unable to parse string as an integer"
)
OWNER_CHANGE_OWNER_NOT_FOUND = "Owner not found"
PET_ALREADY_EXIST_TEXT = "This owner already has a pet with this name"
OWNER_NOT_FOUND_TEXT = "Owner not found"
PET_NO_TYPE_TEXT = "String should have at least 2 characters"
PET_NO_AGE_TEXT = "Input should be a valid integer"
VET_IS_BUSY_TEXT = "Vet already has an appointment at this time"
