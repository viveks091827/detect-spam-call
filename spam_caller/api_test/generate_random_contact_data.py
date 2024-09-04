import requests
import random
import uuid

BASE_URL = "http://127.0.0.1:8001"

def authenticate():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "7221786451", "password": "password"})
    response.raise_for_status() 
    return response.json()['Token']


def get_users(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
    response.raise_for_status()
    return response.json()


def create_contact(token, contact_data):
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(f"{BASE_URL}/api/contact/contact_create/", headers=headers, json=contact_data)
    response.raise_for_status()  
    return response.json()


def generate_random_data():
    return {
        "name": f"Contact_{uuid.uuid4().hex[:2]}",
        "phone_number": random.randint(1000000000, 9999999999)
    }

def main():
    token = authenticate()
    print('token: ', token)

    users = get_users(token)
    print('users: ', users)
    for user in users:
        num_contacts = random.randint(0, 20)
        for _ in range(num_contacts):
            contact_data = generate_random_data()
            contact_data['user_id'] = user['id']
            response = create_contact(token, contact_data)
            print('response: ', response)

if __name__ == "__main__":
    main()
