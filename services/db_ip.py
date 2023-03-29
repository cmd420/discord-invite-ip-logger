import requests
from services.ip_lookup import IpLookup


class DBIP(IpLookup):
    def __init__(self, ip_addr):
        self.url = 'https://api.db-ip.com/v2/free/'
        self.ip_addr = ip_addr

    def lookup_ip(self):
        response = requests.get(self.url + self.ip_addr)
        data = response.json()
        field = {
            "name": "DB IP",
            "value": None
        }

        if 'errorCode' in data:
            field["value"] = "failed"
            return field

        field["value"] = f'IP: {self.ip_addr}\nCountry: {data["countryName"]}\nCity: {data["city"]}'
        return field
