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

