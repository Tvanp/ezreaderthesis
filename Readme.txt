Hi, welcome to my git project.

In order to run the code, execute "simscript.py". 
This code requires a few datasets.

First, it requires a corpus which has word frequency data.
I reccommend the BNC corpus, which I have also used in my thesis.
This is called "df" in the code.

Second, it requires a corpus over which to run the simulation.
I used the GECO corpus. This file is called "corpus" in the code.

Third, you will need empirical data for mono- and bi-linguals.
For this code it is probably best to use the GECO corpus, as it
already has empirical data for mono- and bi-linguals.
The files are called "skipdataBi" and "skipdataMono" in the code.

Lastly, you will need to download the BNC trigrams through python.
If this file is too big (i.e. requires too much PC memory), try using 
a smaller tri-gram corpus like Brown corpus.

____________________________________________________________________________

Notes: The corpi used in the project are very big (especially the n-grams),
it requires a good PC to run this smoothly.

Using different corpi may lead to required code changes in "simscript.py".