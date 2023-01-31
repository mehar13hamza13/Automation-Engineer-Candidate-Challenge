import requests
import json
from datetime import datetime


def get_people_data():
    people_url = 'https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/people/'
    headers = {'Authorization': 'Bearer fFz8Z7OpPTSY7gpAFPrWntoMuo07ACjp'}
    res = requests.get(people_url, headers=headers)
    data = json.loads(res.text)
    return data


def remove_spaces(string):
    return string.strip()


def reformat_date(date_str):
    date_str = datetime.strptime(date_str, '%d-%m-%Y').date()
    return date_str.strftime('%Y-%m-%d')


def create_contact_data(peoples):
    contact_data = []
    for people in peoples:
        contact_data.append(
            {
                "first_name": remove_spaces(people['fields']['firstName']),
                "last_name": remove_spaces(people['fields']['lastName']),
                "birthdate": reformat_date(people['fields']['dateOfBirth']),
                "email": people['fields']['email'],
                "custom_properties": {
                    "airtable_id": people['id'],
                    "lifetime_value": people['fields']['lifetime_value'].split("$")[1]
                }
            }
        )
    return contact_data


def post_contacts(contact_data):
    contact_url = "https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/contacts/"
    username = "datacose"
    password = "196D1115456D7"
    completion_status = True

    for contact in contact_data:
        response = requests.post(contact_url, auth=(username, password), json=contact)
        if response.status_code != 200:
            completion_status = False

    return completion_status


if __name__ == '__main__':
    people_data = get_people_data()
    contacts = create_contact_data(people_data)
    post_contacts(contacts)
