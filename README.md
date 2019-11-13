# codenames-board-generator

This repo cotains two things to deal with Codenames board generation: [command line tool](https://github.com/cekc/codenames-board-generator/blob/master/cli.py) and [flask web app](https://github.com/cekc/codenames-board-generator/blob/master/flask_app.py).

They take a list of words and output PDF like [this](https://github.com/cekc/codenames-board-generator/blob/master/sample.pdf).

## Command line tool

Should work with Python `>=3.5`

### Usage

+ Clone this repo
+ Install requirements with pip: `sudo python3 -m pip install -r requirements-cli.txt` (or make a venv)
+ Run the script [`cli.py`](https://github.com/cekc/codenames-board-generator/blob/master/cli.py), for example
```
python3 cli.py --count 3 --shuffle -i wordlists/ru/original.txt -o sample.pdf
```

## Web app

[An instance I deployed on **pythonanywhere**](http://cekc.pythonanywhere.com/)

