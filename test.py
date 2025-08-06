import jwt
import requests

key = "7020513934"


def user_input():
    url = "http://localhost:6565/verify"
    email = input("Enter you email:")
    encoded = jwt.encode({"email": email}, key, algorithm="HS256")
    response = jwt.decode(encoded, key, algorithms="HS256")
    print(response)
    payload = response
    send = requests.post(url, data=payload)
    print(send)
    return True


user_input()
