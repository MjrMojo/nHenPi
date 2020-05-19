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

## The Visualiser

Just having a text file with the results in it isn't as motivating as being able
to scroll through π seeing the doujins that ocurr. So I made the visualiser. I 
spent far too long on this... I even modified the nHentai logo to have a π 
symbol in it.

![Screenshot of Visualiser](nHentaiVisualiseri/sample_image.png)

To run it you will have to download the nHenPiVisualiser folder and click
`visualiser.html`. I would host it on a website but nHentai (qute fairly) does
not allow their images to be loaded on other websites. Hover over the brackets
to see the cover and title, clicking the cover will take you to it. The 
different bracket colours mean nothing. They're just there to make it easier to
distinguish between different doujins in close proximity. 

Additionally, don't scroll too fast to the right as things get a bit laggy.
Note that this is supported on desktop based platforms with the ability to
scroll. Maybe I'll add further support later but I've sunk a lot of time into
this and I just want to be free from it...

## To Do (?)
- Logging where in π the doujin is found, including any duplicates
- Run the system on 1250000 digits of π data set
