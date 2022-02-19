import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# ====================
@app.route('/')
def index():

    render_template('index.html')

@app.route('/go')
def go():
    
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    gChromeOptions.add_argument("disable-dev-shm-usage")
    gDriver = webdriver.Chrome(
        chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
    )
    gDriver.get("https://www.python.org/")
    time.sleep(3)
    gDriver.close()
    return jsonify("DONE.")

# ====================
if __name__ == "__main__":

    app.run(debug=True)
