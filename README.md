## SEPITIN
<sup>Suomeksi Esitetyt Petruksen & Iikan Tietokoneen Ideoimat Novellit</sup>

[Initial system description](https://github.com/fergusq/sepitin/blob/master/system.md)

[Final system description](https://github.com/fergusq/sepitin/blob/master/sepitin-final-system-description.md)

Surface realizer can be found in directory *harry*, plot generator in *juono* and if you want to see the scripts used to scrape the training data, take a look in *aooo*.

* * *

### Using Juono

Running juono is quite straightforward:

1. Clone the repo and navigate to the *juono* folder

2. Create the virtual environment: `python -m venv venv`

3. Switch to the venv: `source venv/bin/activate`

4. Install the requirements: `pip install -r requirements.txt`

5. Run the script! `python juono.py`

Modifying the script to your needs should be simple enough, I hope the comments are answer to any questions

### Using Harry

1. Clone the repo and navigate to the *harry* folder

2. Download (too large for github, ~420MB) the trained model *aooo.pth* and place it in the *harry/models* folder

3. Create the virtual environment: `python -m venv venv`

4. Switch to the venv: `source venv/bin/activate`

5. Install the requirements: `pip install -r requirements.txt`

6. Run `python predict.py sp-aooo-10k txl,1,aooo`

7. Now you can give some parameters, I'd suggest
  * A token limit of 400: `/n 400`
  * A repetition penalty of 0.8: `/repe 0.8`

8. This will be expanded soon


