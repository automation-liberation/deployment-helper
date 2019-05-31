import requests


def send_changelog_entry(entry):
    url = 'https://api.johansson.tech/changelog'
    response = requests.post(url, data=entry)
    print(response.json())
