# How many nHentai doujins are there in Pi?

Probably no one else has ever asked this question before... for good reason.
It's a weird question to ask. However, just becuase a question is weird, does
not mean it isn't worth spending a Monday evening answering it.

God, I'm a degenerate.

## Results

- In the first 1000 digits of π there are 327 unique, valid nHentai doujins.
- In the first 10,000 digits of π there are 3092 unique, valid nHentai doujins.
  239 of these are in English, 1948 are in Japanese, 360 are in Chinese, and 1
  is speechless. That does leave 544 entries unaccounted for, these fall into
  the category of 'rewrite' and 'translated'. However, there are 544 of them and
  I don't want to categorise them by hand.

## Instructions for replication

On a Linux based system or WSL
```
git clone https://github.com/MjrMojo/nHenPi.git
cd nHenPi
python3 nHenPi.py
```

On Windows, clone the repo and run Python via commandline or your favourite
Python IDE.

To switch between different lengths of π, change either the file loaded on
line 30 for one of the files containing the digits of π available 
[here](https://thestarman.pcministry.com/math/pi/picalcs.htm). Or comment out
lines 29-31 and uncomment line 27 to run it with the first 1000 digits of π.

To run the code for a more recent version of the code, possibly discovering
newly uploaded doujins that occur in π, alter line 23 to be the key of the most
recently uploaded doujin to nHentai.

## To Do (?)
- Make the output a little more friendly?
- Automatic statistics generation with time stamping
- Logging where in π the doujin is found, including any duplicates
- Run the system on 1250000 digits of π data set
