from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.parent
FILES_FOLDER = ROOT_FOLDER / "files"
ICON_FOLDER = FILES_FOLDER / "icon.png"

BIG_SIZE_FONT = 40
MEDIUM_SIZE_FONT = 20
SMALL_SIZE_FONT = 12

PRIMARY_COLOR = "#616161"
SECONDARY_COLOR = "#474747"
DARKEST_PRIMARY_COLOR = "#121212"





FONT = (f"""            Info {{
                            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif; \n
                            font-size: {SMALL_SIZE_FONT}px; \n
                            color: white; \n
                          }}"""
)

qss = f"""
                        QPushButton[cssClass="specialButton"] {{
                            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif; \n
                            color: #fff;
                            background: {PRIMARY_COLOR}; \n
                            border-radius: 5px; \n
                          }}
                        QPushButton[cssClass="specialButton"]:hover {{
                            color: #fff; \n
                            background: {SECONDARY_COLOR}; \n
                          }}
                        QPushButton[cssClass="specialButton"]:pressed {{
                            color: #fff; \n
                            background: {DARKEST_PRIMARY_COLOR}; \n
                          }}"""



STYLESHEET_DISPLAY = f"""Display {{
                              font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif; \n
                              font-weight: 500; \n
                              font-size: {BIG_SIZE_FONT}px; \n
                              color: #fff; \n
                              background-color: rgb(28,28,30); \n
                              box-shadow: 0 0 .4vw rgba(0,0,0,0.5), 0 0 0 .15vw transparent; \n
                              border-radius: 0.4vw; \n
                              border: none; \n
                              outline: none; \n
                              padding: 0.4vw; \n
                              transition: .4s; \n
                            }}

                        Display:hover {{
                              box-shadow: 0 0 0 .15vw rgba(135, 207, 235, 0.186); \n
                            }}

                        Display:focus {{
                              box-shadow: 0 0 0 .15vw skyblue; \n
                            }}"""