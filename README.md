# Wordle Wizard

Wordle Wizard is a bot that can speed-solve Wordle puzzles.

See doesn't understand English, but has the full list of allowed words memorised and is really fast at maths.

Wordle Wizard is aware that she could cheat if she wanted to—by getting the solution for each day from the source code on the Wordle site—but she chooses not to and plays just like you and me by entering her best guesses using the buttons on the site.

## How to use

I haven't been able to come up with a convenient way to make Wordle Wizard available for public consumption yet. Ideally I would like to set up a website where users can click a button and watch Wordle Wizard do her thing live, but I wasn't able to do this easily using Flask on Heroku as Heroku doesn't seem to support display servers like xvfb. Please get in touch if you have any ideas of a good/quick way to showcase the project other than posting screen captures to YouTube.

Those with Python and Chrome installed on their computers can run the program as follows:

1. Clone this repo
2. Get the appropriate version of ChromeDriver for https://chromedriver.chromium.org/downloads and place the chromedriver.exe executable in the wordle_wizard directory.
3. Install the requirements in requirements.txt.
```
pip install -r requirements.txt
```
4. Run play_wordle.py
```
python play_wordle.py
```

## How it works/background to the project

Wordle Wizard came about when I was learning the selenium library in Python and started thinking of fun things to try doing with it. The code for manipulating the browser using selenium is in the WordleController class in the wordle_controller.py module.

The other part of the program is the algorithm for coming up with 'best' guesses each time based on the words currently available. This is implemented in the WordleGame class in wordle_solver.py. The algorithm is simply my best attempt at an efficient Wordle strategy and I created any rigourous tests or proofs to demonstrate that it is optimal, so I would welcome and feedback or suggestions for improvements.

The two classes interact with each other in the main program, play_wordle.py.