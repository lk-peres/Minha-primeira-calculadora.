from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, Signal
from utils.variables import *
from utils.functions import isNumberOrDot, isEmpty, nextNumberIsValid, isInteger


class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Calculadora")
        self._centraWidget = QWidget()
        self.setCentralWidget(self._centraWidget)
        self.vBoxLayout = QVBoxLayout()
        self._centraWidget.setLayout(self.vBoxLayout)

    def addWidgetToVBoxLayout(self, widget : QWidget):
        self.vBoxLayout.addWidget(widget)

    def toAdjustedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def makeMessageBox(self):
        return QMessageBox(self)

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

    def configureStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_SIZE_FONT)
        self.setFont(font)
        self.setMinimumSize(50, 50)

class Display(QLineEdit):
    eqPressed = Signal()
    clearPressed = Signal()
    delPressed = Signal()
    operatorPressed = Signal(str)
    inputPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def configureStyle(self):
        self.setStyleSheet(STYLESHEET_DISPLAY)

    def keyPressEvent(self, event: QKeyEvent):
        text = event.text().strip()
        key = event.key()
        KEY = Qt.Key
        isEnter = key in (KEY.Key_Return, KEY.Key_Enter, KEY.Key_Equal)
        isBackspace = key in (KEY.Key_Backspace, KEY.Key_Delete)
        isEscape = key in (KEY.Key_Escape, KEY.Key_C)
        plus = key == KEY.Key_Plus
        minus = key == KEY.Key_Minus
        asterisk = key == KEY.Key_Asterisk
        bar = key == KEY.Key_Slash
        exponential = key == KEY.Key_Acircumflex
        isNumeric = isNumberOrDot(text)
        isOperator = key in (KEY.Key_Plus, KEY.Key_Minus, KEY.Key_Slash, KEY.Key_Asterisk, KEY.Key_P)

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()

        elif isBackspace:
            self.delPressed.emit()
            return event.ignore()

        elif isEscape:
            self.clearPressed.emit()
            return event.ignore()

        elif isNumeric:
            self.inputPressed.emit(text)
            return event.ignore()

        elif isOperator:

            if text.lower() == "p":
                text = "^"
            self.operatorPressed.emit(text)
            return event.ignore()

        elif isEmpty(text):
            return event.ignore()

class Info(QLabel):
    def __init__(self, text : str, parent : QWidget | None = None):
        super(Info, self).__init__(text, parent)
        self.setText(text)

    def configureStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setStyleSheet(FONT)

class GridButtons(QGridLayout):
    def __init__(self, display : Display, info : Info, window : MyWindow, *args, **kwargs):
        super(GridButtons, self).__init__(*args, **kwargs)
        self._makeGrid = [
            ["C", "⌫", "^", "="],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            [".", "0", "N", "/"],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationValueInitial = "Sua conta"
        self.equation = self._equationValueInitial
        self._op = ""
        self._numberLeft = ""
        self._numberRight = ""
        self._makeButtonsGrid()

    @property
    def equation(self):
        return self._equation
    @equation.setter
    def equation(self, value: str):
        self._equation = value
        self.info.setText(value)

    def _makeButtonsGrid(self):
        self.display.eqPressed.connect(self._equationResult)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.operatorPressed.connect(self._configureOperator)
        self.display.inputPressed.connect(self._insertTextInDisplay)
        for row, rowButtons in enumerate(self._makeGrid):
            for col, buttonText in enumerate(rowButtons):
                button = Button(buttonText)
                invalidButton = isEmpty(buttonText)

                if not isNumberOrDot(buttonText) and not invalidButton:
                    button.setProperty('cssClass', 'specialButton')
                    self._configureEspecialButton(button)

                slot = self._makeButtonSlot(self._insertTextInDisplay, buttonText, )
                button.configureStyle()
                self.addWidget(button, row, col)
                self._configureConnectClicked(button, slot)

    def _configureConnectClicked(self, button: QPushButton, slot):
        button.clicked.connect(slot)

    def _makeButtonSlot(self, method, *args, **kwargs):
        @Slot()
        def buttonSlot(_):
            return method(*args, **kwargs)
        return buttonSlot

    def _insertTextInDisplay(self, text: str) -> None:
        displayText = self.display.text()
        newDisplayText = displayText + text
        invalidNumber = nextNumberIsValid(newDisplayText)

        if invalidNumber:
            self.display.insert(text)

    def _configureEspecialButton(self, button: QPushButton):
        buttonText = button.text()

        if buttonText in '+-*/^':
            self._configureConnectClicked(button, self._makeButtonSlot(self._configureOperator, buttonText))

        elif buttonText == '=':
            self._configureConnectClicked(button, self._makeButtonSlot(self._equationResult))

        elif buttonText == 'C':
            self._configureConnectClicked(button, self._makeButtonSlot(self._clear))

        elif buttonText == "⌫":
            self._configureConnectClicked(button, self._makeButtonSlot(self.display.backspace))

        elif buttonText == "N":
            self._configureConnectClicked(button, self._makeButtonSlot(self._convertNumber))

    def _convertNumber(self):
        text = self.display.text()

        if isEmpty(text):
            return

        number = str(-float(text))
        text = isInteger(number)
        self.display.setText(text)

    def _configureOperator(self, operator: str):
        displayText = self.display.text()
        invalidDisplay = isEmpty(displayText)
        invalidNumberLeft = isEmpty(self._numberLeft)

        if not invalidDisplay and invalidNumberLeft:
            self._numberLeft = displayText
            self._op = operator
            self.equation = f"{displayText} {operator}"
            self.display.clear()
            return

        elif invalidDisplay and invalidNumberLeft:
            self._showMessage("Precisa digitar numero.")
            return

        elif not invalidNumberLeft and not invalidDisplay:
            self._numberRight = displayText
            self._equationResult()
            newDisplayText = self.display.text()
            self._op = operator
            self._numberLeft = newDisplayText
            self.equation = f"{newDisplayText} {operator}"
            self.display.clear()
            return

        else:
            self.equation = f"{self._numberLeft} {operator}"
            self._op = operator

    def _equationResult(self):
        displayText = self.display.text()
        infoText = self.info.text()
        invalidText = isEmpty(displayText)
        invalidNumberLeft = isEmpty(self._numberLeft)
        invalidOperator = isEmpty(self._op)

        if not invalidText and not invalidNumberLeft and not invalidOperator:
            self._numberRight = displayText
            self.equation = f"{infoText} {displayText} ="
            numberLeft = float(self._numberLeft)
            numberRight = float(self._numberRight)

            if self._op == '+':
                self._sum(numberLeft, numberRight)

            elif self._op == '-':
                self._subtraction(numberLeft, numberRight)

            elif self._op == '*':
                self._multiply(numberLeft, numberRight)

            elif self._op == '/':
                self._divide(numberLeft, numberRight)

            else:
                self._potentiation(numberLeft, numberRight)
            return

        self._showMessage("Nenhum numero digitado!")

    def _sum(self, numberLeft: float, numberRight: float):
        total = f"{numberLeft + numberRight}"
        total = isInteger(total)
        return self._showResult(total)

    def _subtraction(self, numberLeft: float, numberRight: float):
        total = f"{numberLeft - numberRight}"
        total = isInteger(total)
        return self._showResult(total)

    def _multiply(self, numberLeft: float, numberRight: float):
        total = f"{numberLeft * numberRight}"
        total = isInteger(total)
        return self._showResult(total)

    def _divide(self, numberLeft: float, numberRight: float):

        if numberRight == 0:
            self._showError("Não pode dividir um numero por zero.")
            return self._showResult("0")

        total = f"{numberLeft / numberRight}"
        total = isInteger(total)
        return self._showResult(total)

    def _potentiation(self, numberLeft: float, numberRight: float):

        try:
            total = f"{numberLeft ** numberRight}"

        except OverflowError:
            self._showError("Essa conta não pode ser realizada.")
            total = "0"

        total = isInteger(total)
        return self._showResult(total)

    def _showResult(self, total: str):
        self._clearOperation()
        self.display.setText(total)

    def _clear(self) -> None:
        self._clearOperation()
        self.display.clear()
        self.equation = self._equationValueInitial

    def _clearOperation(self) -> None:
        self._op = ""
        self._numberLeft = ""
        self._numberRight = ""

    def _showMessage(self, message: str) -> None:
        msgBox = self.window.makeMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(msgBox.Icon.Warning)
        msgBox.exec()

    def _showError(self, text: str) -> None:
        msgBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()