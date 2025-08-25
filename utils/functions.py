import re
import qdarkstyle
from utils.variables import qss

def setupTheme(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    app.setStyleSheet(app.styleSheet() + qss)


NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumberOrDot(button_text : str) -> bool:
    return bool(NUM_OR_DOT_REGEX.search(button_text))

def nextNumberIsValid(string: str) -> bool:
    valid = False
    try:
        float(string)
        valid = True
        return valid
    except ValueError:
        return valid

def isEmpty(button_text : str) -> bool:
    return len(button_text) == 0

def isInteger(text : str) -> str:
    number = float(text)
    if number.is_integer():
        number = int(number)
    return str(number)