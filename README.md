## Synopsis

Extract ticket info from a .pkpass (Apple Wallet ticket filetype). And generate a Ticketmaster-equivalent QR code from the extracted info by using the Google API.

## Code Example

Just set `PASS` on line 10 and everything will hopefully work (after running `python main.py`).

## Dependencies

I think `requests` is the only thing that needs to be `pip` installed? Here's a full list of what I import:

```
import zipfile
import shutil
import json
import os
import requests
```
