import datetime as dt
import requests
from django.conf import settings
import pytz
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import MessageSerializer
from api.models import Token


def get_token():
    instance = Token.objects.first()

    if not instance:
        print('enter token to db')
        return

    # refresh token if expire
    current_date = dt.datetime.today()
    expire_date = instance.modified_at + dt.timedelta(0, instance.expires_in)

    utc = pytz.UTC
    if current_date.replace(tzinfo=utc) > expire_date.replace(tzinfo=utc):
        data = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": instance.refresh,
            "redirect_uri": settings.REDIRECT_URI
        }
        r = requests.post(settings.REFRESH_TOKEN_URL, data=data)
        answer = r.json()
        instance.access = answer["access_token"]
        instance.refresh = answer["refresh_token"]
        instance.expires_in = answer["expires_in"]
        instance.save()

    return instance.access


def find_contact(email, phone):
    def query_contact(key):
        token = get_token()
        headers = {"Authorization": "Bearer {}".format(token)}
        url = "https://zzzarchibald.amocrm.ru/api/v4/contacts"
        params = {"query": key}
        r = requests.get(url=url, params=params, headers=headers)
        if r.status_code == 200:
            answer = r.json()
            return answer["_embedded"]["contacts"][0]["id"]

    # find by phone if success, return contact id
    e = query_contact(phone)
    if e:
        return e
    # find by email if success, return contact id
    p = query_contact(email)
    if p:
        return p


def create_contact(email, phone, name):
    token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://zzzarchibald.amocrm.ru/api/v4/contacts"
    data = [
        {
            "name": name,
            "custom_fields_values": [
                {
                    "field_id": 807651,
                    "field_name": "Телефон",
                    "values": [
                        {
                            "value": phone,
                            "enum_code": "WORK"
                        }
                    ]
                },
                {
                    "field_id": 807653,
                    "field_name": "Email",
                    "values": [
                        {
                            "value": email,
                            "enum_code": "WORK"
                        }
                    ]
                }
           ]
        }
    ]
    r = requests.post(url=url, json=data, headers=headers)
    if r.status_code == 200:
        answer = r.json()
        return answer["_embedded"]["contacts"][0]["id"]


def update_contact(contact_id, email, phone, name):
    token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://zzzarchibald.amocrm.ru/api/v4/contacts/{}".format(contact_id)
    data = {
        "name": name,
        "custom_fields_values": [
            {
                "field_id": 807651,
                "field_name": "Телефон",
                "values": [
                    {
                        "value": phone,
                        "enum_code": "WORK"
                    }
                ]
            },
            {
                "field_id": 807653,
                "field_name": "Email",
                "values": [
                    {
                        "value": email,
                        "enum_code": "WORK"
                    }
                ]
            }
       ]
    }
    r = requests.patch(url=url, json=data, headers=headers)


def create_deal(contact_id):
    token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://zzzarchibald.amocrm.ru/api/v4/leads"
    data = [
        {
            "_embedded": {
                "contacts": [
                    {
                        "id": contact_id
                    }
                ]
            }
        }
    ]
    r = requests.post(url=url, json=data, headers=headers)
    answer = r.json()
    return answer

class CreateLead(APIView):
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['phone'] = serializer.validated_data['phone'].national_number

        email = serializer.validated_data['email']
        phone = serializer.validated_data['phone']
        name = serializer.validated_data['name']

        contact_id = find_contact(email, phone)
        if contact_id:
            update_contact(contact_id, email, phone, name)
        else:
            contact_id = create_contact(email, phone, name)

        answer = create_deal(contact_id)

        return Response(answer)
