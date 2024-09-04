import requests
import random
import uuid

BASE_URL = "http://127.0.0.1:8001"

def register(data):
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    response.raise_for_status() 
    return response.json()



def generate_random_data():
    return {
        'name': f'Contact_{uuid.uuid4().hex[:2]}',
        'phone_number': random.randint(1000000000, 9999999999),
        'email': f'Contact_{uuid.uuid4().hex[:2]}@gmail.com',
        'password': 'password'
    }


def main():

    data_list = [generate_random_data() for _ in range(100)]

    for data in data_list:
            response = register(data)
            print('response: ', response)

if __name__ == "__main__":
    main()
