import PyQt5.QtWidgets as qt
from functools import partial
import json

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300
WINDOW_NAME = "Find match from product offer title"

DEFAULT_PRODUCT_TITLE = "Apple iPhone 4 8GB SIM-Free - Black"
DEFAULT_JSON_RESULT = "{\"name\": \"Gilbert\", \"wins\": [[\"straight\", \"7♣\"], [\"one pair\", \"10♥\"]]}"


def displayJsonResult(productTitleBox, textAreaToDisplayResult):
    productTitle = productTitleBox.text()
    result = "{}"

    # get json
    print("Getting json for '{}'".format(productTitle))

    result = json.loads(result)
    parsed_result = json.dumps(result, indent=4, sort_keys=False)

    textAreaToDisplayResult.setPlainText(parsed_result)


app = qt.QApplication([])
window = qt.QWidget()
window.setWindowTitle(WINDOW_NAME)

# Set default contents
parsed_json = json.loads(DEFAULT_JSON_RESULT)
parsed_json = json.dumps(parsed_json, indent=4, sort_keys=False)

# Widgets
label = qt.QLabel('Product title: ')
productOfferTitleTextBox = qt.QLineEdit(DEFAULT_PRODUCT_TITLE)
findMatchBtn = qt.QPushButton('Find Match')
jsonResultDisplayTextArea = qt.QPlainTextEdit(parsed_json)
jsonResultDisplayTextArea.setReadOnly(True)

# Set click event hanlder function for button
findMatchBtn.clicked.connect(partial(displayJsonResult, 
                                     productOfferTitleTextBox,
                                     jsonResultDisplayTextArea))

# Top panel
topLayout = qt.QHBoxLayout()
topLayout.addWidget(label)
topLayout.addWidget(productOfferTitleTextBox)
topLayout.addWidget(findMatchBtn)

# Main panel
mainLayout = qt.QVBoxLayout()
mainLayout.addLayout(topLayout)
mainLayout.addWidget(jsonResultDisplayTextArea)

window.setLayout(mainLayout)
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.show()

# Run the app until it is closed by the user
app.exec_()
