"""imports
    """
import datetime


def log(message: str, color: str = 'default'):
    """This is a very basic logger, used to log thing with some fancy color-coding and timestamps.

    Args:
        message (str): The message you want to log.
        color (str, optional): The color 
        you want the message to be displayed in. Defaults to 'default', which is a blue-ish color.
    """
    if color == 'default':
        color = '\033[96m'  # These are escape characters for color coding
    if color == 'green':
        color = '\033[92m'
    if color == 'red':
        color = '\033[91m'
    if color == 'yellow':
        color = '\033[93m'
    print(color + "[" + str(datetime.datetime.now()) +
          "] magicaltavern: " + str(message) + '\033[96m')
