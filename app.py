import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# ====================
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/go')
def go():
    
    print('YO!')
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    gChromeOptions.add_argument("disable-dev-shm-usage")
    gChromeOptions.add_argument("--no-sandbox")
    gDriver = webdriver.Chrome(
        chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
    )
    gDriver.minimize_window()
    gDriver.maximize_window()
    gDriver.get("https://www.python.org/")
    gDriver.switch_to.window(gDriver.current_window_handle)
    time.sleep(10)
    gDriver.close()
    return (jsonify("DONE."))

# ====================
if __name__ == "__main__":

    app.run(debug=True)
