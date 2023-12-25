from faker import Faker
import random


def generate_fake_contacts_data(count=1):
    res = []
    fake = Faker()
    for _ in range(0, count):
        res.append(
            {
                "name": fake.name(),
                "phone": random_phone(),
                "birthday": fake.date_object().strftime("%d.%m.%Y"),
                "email": fake.email(),
                "address": fake.address(),
            }
        )
    return res


def random_phone():
    random_numbers = [random.randint(1, 9) for _ in range(10)]
    return "".join(map(str, random_numbers))
