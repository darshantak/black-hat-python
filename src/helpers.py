import requests
import time
from stem import Signal
from stem.control import Controller


def get_current_ip():
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'

    try:
        r = session.get('http://httpbin.org/ip')
    except Exception as e:
        print (str(e))
    else:
        return r.text


def renew_tor_ip():
    with Controller.from_port(port = 9050) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


if __name__ == "__main__":
    # time.sleep(50000)
    for i in range(5):
        print( get_current_ip())
        renew_tor_ip()
        time.sleep(10)