import argparse
from psycopg2 import connect, OperationalError
from models import users
from models import messages
from clcrypto import check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-l", "--list", help="text message")
parser.add_argument("-s", "--send", help="send message")
args = parser.parse_args()


def print_user_messages(cur, users):
    message_s = messages.load_all_messages(cur, user.id)
    for message in message_s:
        from_ = users.load_user_by_id(cur, message.from_id)
        print(20 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(20 * "-")


def send_message(cur, from_id, recipient_name, text):
    if len(text) > 255:
        print("Message is too long!")
        return
    to = users.load_user_by_username(cur, recipient_name)
    if to:
        message = messages(from_id, to.id, text=text)
        message.save_to_db(cur)
        print("Message send")
    else:
        print("Recipient does not exists.")


if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = users.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)
