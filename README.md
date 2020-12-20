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

2. [Download](https://dropper.link/stream/-2MV4W4.pth) (too large for github, ~420MB) the trained model *aooo.pth* and place it in the *harry/models* folder

3. Create the virtual environment: `python -m venv venv`

4. Switch to the venv: `source venv/bin/activate`

5. Install the requirements: `pip install -r requirements.txt`

6. Run `python predict.py sp-aooo-10k txl,1,aooo`

7. Now you can give some parameters, I'd suggest:
  * A token limit of 400: `/n 400`
  * A repetition penalty of 0.8: `/repe 0.8`

8. Give a prompt, for example: `Draco oli suunitellut tätä koko loman ajan, ja tänään hän aikoi tehdä sen. Hän aikoi nolata Harryn Ginnyn ja kaikkien muiden edessä totaalisesti. br "Tiedätkös, minusta sinun ei kannattaisi luulla liikoja itsestäsi", Draco naurahti Harrylle.` Use `br` for line breaks. `xxbos` is a special character that signifies the beginning of a new story. If you want a new stroy with no given prompt you can just type `xxbos`

### Using the dialogue generator

1. Do steps 1 to 5 of the above instructions

2. Install the Festival Speech Synthesis System

3. Install the Finnish voice packs *hy_fi_mv_diphone* and *suo_fi_lj_diphone*, `apt install festvox-suopuhe-{lj,mv}` should do the trick

4. Run the script and give it some dialogue to begin, for example: `perl6 aooodialogi.p6 'Draco naurahti Harrylle: "Tiedätkös, minusta sinun ei kannattaisi luulla liikoja itsestäsi" br Harry kavahti: "Hah, mitä tarkoitat? Sitä paitsi sinun on turha väittää muita ylimielisiksi, Draco" br Draco sanoi: "Ginny ei kuitenkaan tahdo olla tanssiparisi, nolaat vain itsesi"'`



