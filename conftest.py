import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


def generate_order_data(color=None):
    def random_phone():
        return "+7" + ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    data = {
        "firstName": generate_random_string(10),
        "lastName": generate_random_string(10),
        "address": generate_random_string(20),
        "metroStation": random.randint(1, 10),
        "phone": random_phone(),
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2024-12-31",
        "comment": generate_random_string(20)
    }
    
    if color is not None:
        if isinstance(color, list):
            data["color"] = color
        else:
            data["color"] = [color]
    
    return data