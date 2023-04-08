import requests
from services.ip_lookup import IpLookup

class IpApi(IpLookup):
    def __init__(self, ip_addr):
        self.url = 'http://ip-api.com/json/'
        self.ip_addr = ip_addr

    def lookup_ip(self):
        response = requests.get(self.url + self.ip_addr)
        data = response.json()
        field = {
            "name": "Ip Api",
            "value": None
        }

        if data["status"] == "fail":
            field["value"] = "failed"
            return field

        field["value"] = f'IP: {self.ip_addr}\nCountry: {data["country"]}\nCity: {data["city"]}\n' + \
            f'Lat, Lon: {data["lat"]}, {data["lon"]}\nTimezone: {data["timezone"]}\nISP: {data["isp"]}'

        return field
