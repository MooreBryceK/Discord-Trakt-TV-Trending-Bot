import requests
import auth
import json


# Run this function to setup trakt tv api app
def setup_authentication():
    authentication_successful = False
    if get_device_and_user_code():
        input('Click on verification url hyperlink, enter user code and press any key to continue... ')
        if authenticate_device():
            print('Authentication Successful')
            authentication_successful = True
    return authentication_successful


# Post request to get device and user code, returns true if successful
def get_device_and_user_code():
    body = {
        'client_id': auth.TRAKT_CLIENT_ID
    }
    headers = {
        'content-type': 'application/json'
    }
    url = 'https://api.trakt.tv/oauth/device/code'
    response = requests.post(url, data=json.dumps(body), headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)

    return response.status_code == 200


# Get request to authenticate device with trakt tv api
def authenticate_device():
    url = f'https://trakt.tv/oauth/authorize?response_type=code'
    url += f'&client_id={auth.TRAKT_CLIENT_ID}'
    url += f'&redirect_uri={auth.TRAKT_REDIRECT_URI}'

    response = requests.get(url)
    return response.status_code == 200


# Get request for trending shows or movies on trakt tv api
def get_trakt_trending(media):
    url = f'https://api.trakt.tv/{media}/trending'
    headers = {
        'content-type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': auth.TRAKT_CLIENT_ID
    }

    response = requests.get(url, headers=headers)
    post = ''
    if response.status_code == 200:
        trending_shows = response.json()
        for show in trending_shows:
            post += f"[{show[media[:-1]]['title']} ({show[media[:-1]]['year']})]"
            post += f"(https://trakt.tv/{media}/{show[media[:-1]]['ids']['slug']})\n"

    return post

