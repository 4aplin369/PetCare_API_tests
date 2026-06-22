import random
import string
import api

from faker import Faker
from datetime import datetime, timedelta, timezone

fake = Faker()


def get_fake_email():
    new_email = fake.email()
    return new_email


def get_fake_fullname():
    new_name = f"{fake.first_name()} {fake.last_name()}"
    return new_name


def get_fake_phone():
    phone = fake.phone_number()
    return phone


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(length))
    return random_string


def get_owner_register_data():
    name = get_fake_fullname()
    email = get_fake_email()
    phone = get_fake_phone()
    return name, email, phone


def get_id_and_delete_owner(response):
    r_json = response.json()
    owner_id = r_json["id"]
    api.owner_delete(owner_id)


def get_id_owner(response):
    r_json = response.json()
    return r_json["id"]


def generate_random_id():
    return random.randint(500, 1500)


def get_pet_register_data(owner_id):
    age = random.randint(0, 12)
    breed = fake.word()
    name = fake.name()
    notes = fake.sentence()
    owner_id = owner_id
    species = random.choice(["cat", "dog", "rabbit"])
    return age, breed, name, notes, owner_id, species


def get_id_and_delete_pet(response):
    r_json = response.json()
    pet_id = r_json["id"]
    api.pet_delete(pet_id)


def delete_many_owners(self):
    while True:
        r = api.get_owners()
        owners = r.json()

        if len(owners) <= 4:
            break

        owner_id = owners[-1]["id"]
        api.owner_delete(owner_id)


def generate_starts_at():
    starts_at = (
        (datetime.now(timezone.utc) + timedelta(days=1))
        .replace(hour=random.randint(8, 22), minute=0, second=0, microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    return starts_at
