import argparse
from psycopg2 import connect, OperationalError
from models import users
from models import messages
from clcrypto import check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="to")
perser.add_argument("-l", "--list", help="text message")
perser.add_argument("-s", "--send", help="send message")
args = parser.parse_args()

def list_message(username, password):
    with connect()
