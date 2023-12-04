from stem import Signal
from stem.control import Controller
import requests
import time

TOR_CONTROL_PORT = 9051  
proxies = {
    'http':'socks5h://127.0.0.1:9050',
    'https':'socks5h://127.0.0.1:9050',
}
def get_current_ip():
    response = requests.get("http://httpbin.org/ip",proxies=proxies)
    return response.json()["origin"]

def change_tor_ip():
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def make_request_using_tor(url):
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate()

        current_ip = get_current_ip()
        print(f"Current IP: {current_ip}")

        with requests.get(url) as response:
            print("Break")

        new_ip = get_current_ip()
        print(f"New IP: {new_ip}")

if __name__ == "__main__":
    tor_url = "https://google.com"
    num_requests = 5

    for _ in range(num_requests):
        make_request_using_tor(tor_url)
        time.sleep(10)  
