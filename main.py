import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from MyApp import MyWindow, Display, Info, GridButtons
from utils.variables import ICON_FOLDER
from utils.functions import setupTheme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MyWindow()

    #ICON
    icon = QIcon(str(ICON_FOLDER))
    app.setWindowIcon(icon)
    window.setWindowIcon(icon)

    #Info
    info = Info("")
    window.addWidgetToVBoxLayout(info)
    info.configureStyle()

    #DISPLAY
    display = Display()
    window.addWidgetToVBoxLayout(display)
    display.configureStyle()

    #Grid
    gridButtons = GridButtons(display, info, window)
    window.vBoxLayout.addLayout(gridButtons)

    window.toAdjustedSize()
    window.show()
    app.exec()