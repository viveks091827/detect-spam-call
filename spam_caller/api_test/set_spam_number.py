import requests
import random
import uuid

BASE_URL = "http://127.0.0.1:8001"

def authenticate():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "7221786451", "password": "password"})
    response.raise_for_status() 
    return response.json()['Token']


def get_contact(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f"{BASE_URL}/api/contact/list", headers=headers)
    response.raise_for_status()
    return response.json()

def get_users(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
    response.raise_for_status()
    return response.json()


def register_spam_number(token, contact_data):
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(f"{BASE_URL}/api/contact/set_spam/", headers=headers, json=contact_data)
    response.raise_for_status()  
    return response.json()


def main():
    token = authenticate()
    print('token: ', token)
    
    users = get_users(token)
    contacts = get_contact(token)
    for contact in contacts:
        phone_number = contact['phone_number']
        user_id = users[random.randint(0, len(users)-1)]['id']
        data = {'phone_number': phone_number, 'user_id': user_id}

        no = random.randint(0, 10)
        if no % 2 == 0:
            response = register_spam_number(token, data)
            print('response: ', response)

if __name__ == "__main__":
    main()
