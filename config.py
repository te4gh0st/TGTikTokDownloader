#  Copyright © 2024 te4gh0st (Vitaliy Timtsurak). All rights reserved.
#  Licensed under the Apache License, Version 2.0

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv("TOKEN", "")

WEBHOOK_ACTIVE: str = os.getenv("WEBHOOK_ACTIVE", "0")
WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST', '')
WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH', '')
WEBAPP_HOST: str = os.getenv('WEBAPP_HOST', 'localhost')
WEBAPP_PORT: str = os.getenv('WEBAPP_PORT', '')

WEBHOOK_URL: str = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

try:
    ADMIN_ID: int = int(os.getenv('ADMIN_ID', '0'))
except TypeError:
    print("Incorrect ADMIN ID")
    exit(-1)
