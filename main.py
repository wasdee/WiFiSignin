import asyncio
from time import sleep
import os
import sys

import delegator
from box import Box
from raven import Client
from raven.handlers.logbook import SentryHandler
from logbook import Logger, StreamHandler

from weblogin import isConnected, login

client = Client(os.environ.get('SENTRY'))
sentry_handler = SentryHandler(client)
sentry_handler.push_application()
StreamHandler(sys.stdout).push_application()
log = Logger('wifi_login')

def get_wifi():
    cmd = r"/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
    c = delegator.run(cmd)
    lines = list(map(str.strip, c.out.splitlines()))
    Wifi = {x[0].strip(): x[1][1:] for x in [l.split(':', 2) for l in lines]}
    return Box(Wifi)

def main():
    while True:
        if not isConnected():
            # wifi = get_wifi()
            log.warn('reconnecting.. wifi')
            asyncio.get_event_loop().run_until_complete( login() )
        sleep(1)
        log.info('wifi is connected.')

if __name__ == '__main__':
    main()
