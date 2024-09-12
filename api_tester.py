import requests
import base64
import json

# Base URL of the API
BASE_URL = "https://gate.ascp.ru:8443/ugt-dev-7/hs/v2/"

# Authentication headers
api_key = "ew0KImFsZyI6ICJIUzI1NiIsDQoidHlwIjogIkpXVCINCn0.ew0KImp0aSI6ICI0YTAxNzE1ZC02N2QwLTQ5ODAtOGY3Yi0xYjYxNDkyMDlhNWYiLA0KImV4cCI6ICIxNzQ1NzMzODgzIiwNCiJhdWQiOiBbDQoid21zIiwNCiJ1Z3QtdGVzdCINCl0sDQoic3ViIjogIkFQSXVzZXIIiwNCiJpYXQiOiAiMTcxNDE5Nzg4MyIsDQoiaXNzIjogInNzbCINCn0.uIknTN0nRxiF0f-I7OUK5GqZtDslXJxn7QWdNeh6Xns"
encoded_basic_auth_creds = "0JDQtNC80LjQvdC40YHRgtGA0LDRgtC+0YA6MTIzNDU2"

# Получение JWT токена
def get_jwt_token():
    url = f"{BASE_URL}auth/login"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "BasicAuth": f"Basic {encoded_basic_auth_creds}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Error obtaining JWT token:", response.json())
        return None


# Получение судозаходов за период
def get_vessel_calls_period(start_date, end_date):
    url = f"{BASE_URL}vesselcalls"
    headers = {

        "Authorization": f"Bearer {api_key}",
        "bearerAuth": f"{get_jwt_token()}",
        
        "Content-Type": "application/json"
    }
    params = {
        "page": 1,
        "pageSize": 10
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching vessel calls:", response.json())
        return None

# Функция для получения списка пользователей клиента
def get_client_users(client_id):
    try:
        token = get_jwt_token()
        url = f"{BASE_URL}clients/{client_id}/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
        
# Функция для получения списка пользователей организации (эндпоинт /users/list)
# Получение списка пользователей организации
# Позволяет получить список всех пользователей, принадлежащих указанной организации.
def get_organization_users(organization_id):
    try:
        token = get_jwt_token()
        url = f"{BASE_URL}users/list"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {"organization_id": organization_id}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
                
if __name__ == "__main__":
    jwt_token = get_jwt_token()
    
    if jwt_token:
        start_date = "2023-01-01"
        end_date = "2023-01-31"
        # vessel_calls = get_vessel_calls_period(start_date, end_date)
        users_list = get_organization_users(0)
        if users_list:
            print(json.dumps(users_list, indent=2, ensure_ascii=False))
