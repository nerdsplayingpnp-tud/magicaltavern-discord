import datetime


def log(message, color='default'):
    if color == 'default':
        color = '\033[96m'
    if color == 'green':
        color = '\033[92m'
    if color == 'red':
        color = '\033[91m'
    if color == 'yellow':
        color = '\033[93m'
    print(color + "[" + str(datetime.datetime.now()) +
          "] magicaltavern: " + str(message) + '\033[96m')
