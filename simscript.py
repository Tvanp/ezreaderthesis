"""
Code for running the simulation
"""

import simpy

import simulation as ez

import pandas as pd

import trigrams as gram

df = pd.read_csv("path to data with word frequency", sep=' ', names =["frequency", "token", "wordtype", "wordID"], skiprows=1) #Word frequency data
corpus = pd.read_csv(r"path to the used corpus", sep=';', skiprows=[i for i in range(1,28853)], nrows=500) #GECO Corpus
skipdataBi = pd.read_csv("path to the data for bilinguals", sep=';', nrows=500)
skipdataMono = pd.read_csv("path to the data for monolinguals", sep=';', skiprows=[i for i in range(1,29957)], nrows=500)

wordlimit = 428 #change this to define to how far the sim will run
#wordlimit = 66: run the first 10 sentences in the corpus, to save processing time
#wordlimit = 428: run first 50 sentences

###################
##Predictability###
###################
words = list(corpus.WORD.head(wordlimit))
from nltk import trigrams

clozeList = []
ngrams = trigrams(words)
for grams in ngrams:
    clozeList.append(gram.calculate_trigram_probability(grams))

#######################################################
###Creating the list of words used in the simulation###
#######################################################

simulation = []
highfreq = []
lowfreq = []
low_passes = 0
high_passes = 0
skipBiHi = 0
skipBiLow = 0
skipMonoHi = 0
skipMonoLow = 0

lines = corpus.head(wordlimit).iterrows()

for index, row in lines: 
    if row[5] in df.token:
        index2 = list(df.token).index(row[3].lower())
        if index == 0 or index == 1:
            simulation.append(ez.Word(corpus.WORD[index],df.frequency[index2],0,25,0.01))
        elif index != 0 and index != 1 and row[1] != corpus.SENTENCE_ID[index-1]:
            simulation.append(ez.Word(corpus.WORD[index],df.frequency[index2],0,25,0.01))
            simulation.append(ez.Word(corpus.WORD[index+1],df.frequency[index2+1],0,25,0.01))
            index += 2
            next(lines,None)
            next(lines,None)
        else:
            simulation.append(ez.Word(corpus.WORD[index],df.frequency[index2],clozeList[index-2],25,0.01))

#Making a set to save the unique words
uniquesim = set(simulation)

for word in uniquesim:
    if word.frequency <= 100000: #Occurrence: lower than 100 in a million
        lowfreq.append(word.token)
    else:
        highfreq.append(word.token)
        
lowfreq.reverse()
highfreq.reverse()

for word in simulation:
    if word.frequency <= 100000:
        low_passes = low_passes + 1
    else:
        high_passes = high_passes + 1

# Empirical data for less proficient readers
for index, row in skipdataBi.head(wordlimit).iterrows():
    if row[12] == 0:
        string = row[10].strip()
        if string in highfreq:
            skipBiHi += 1
        else:
            skipBiLow += 1

#Empirical data
for index, row in skipdataMono.head(wordlimit).iterrows():
    if row[12] == 0:
        string = row[10]
        if string in highfreq:
            skipMonoHi += 1
        else:
            skipMonoLow += 1
        
#Calculating empirical skipping rates
skipBiTot = skipBiLow + skipBiHi
skipMonoTot = skipMonoLow + skipMonoHi

biReaderSkipLow = skipBiLow/low_passes * 100
biReaderSkipHi = skipBiHi/high_passes * 100
biReaderSkipTot = skipBiTot / wordlimit * 100            

monoReaderSkipLow = skipMonoLow/low_passes * 100
monoReaderSkipHi = skipMonoHi/high_passes * 100
monoReaderSkipTot = skipMonoTot/wordlimit * 100

################
###Simulation###
################

total_words = 0
total_skips = 0
percentageskipped = 0
totalskiphigh = 0
totalskiplow = 0
total_low_passes = 0
total_high_passes = 0

empiricalBiSkipLow = 0
empiricalBiSkipHi = 0
empiricalMonoSkipLow = 0
empiricalMonoSkipHi = 0
empiricalMonoSkipTot = 0
empiricalBiSkipTot = 0

for i in range(900): #How many times shall I simulate?
    sim = ez.Simulation(sentence=simulation)
    sleeps_fixated = []
    highest_fixation = 0
    for _ in range(1):
        sim = ez.Simulation(sentence=simulation, realtime=False, trace=False)
        #sim.run(2) #if you want to run the whole simulation
        sleeps_fixated.append(0)
        while True:
            try:
                sim.step()
                if sim.fixated_word and sim.fixation_point >= highest_fixation and sim.fixated_word != sleeps_fixated[-1]:
                    sleeps_fixated.append(str(sim.fixated_word))
            except simpy.core.EmptySchedule:
                break
            highest_fixation = max(highest_fixation, sim.fixation_point)

    skippedwords = []
    counter = 0
    sleeps_fixated.remove(0)

    for i in range(wordlimit): #This loop checks whether or not a word has been skipped
        if sleeps_fixated[counter] != corpus.WORD.head(wordlimit)[i]:
            skippedwords.append(corpus.WORD[i]) #When a word was skipped, it is added to the list of skipped words
            counter = counter - 1
        if counter != len(sleeps_fixated) -1: counter = counter + 1 
    
    #Counting skips of high-and low frequency words
    for i in range(len(skippedwords)):
        if skippedwords[i] in highfreq:
            totalskiphigh = totalskiphigh + 1
        if skippedwords[i] not in highfreq:
            totalskiplow = totalskiplow + 1  
    
    #####################################
    ###Calculating the skip percentage###
    #####################################
    
    total_words = total_words + wordlimit
    total_skips = total_skips + len(skippedwords)
    total_low_passes = total_low_passes + low_passes
    total_high_passes = total_high_passes + high_passes
    percentageskipped = total_skips/total_words * 100
    skipLow = totalskiplow/total_low_passes * 100
    skipHigh = totalskiphigh/total_high_passes * 100
    
print("Total words simulated: " + str(total_words))
print("Total words skipped: " + str(total_skips))
print("Percentage of words skipped: " + str(percentageskipped))
print("Percentage of high frequency words skipped: " + str(skipHigh))
print("Percentage of low frequency words skipped: " + str(skipLow))
print("___________________________________________________")
print("Empirical data from Geco Corpus:")
print("Percentage of low frequency words skipped by less proficient readers " + str(biReaderSkipLow))
print("Percentage of high frequency words skipped by less proficient readers " + str(biReaderSkipHi))
print("Total percentage of words skipped by less proficient readers : " + str(biReaderSkipTot))
print(" ")
print("Percentage of low frequency words skipped by skilled readers " + str(monoReaderSkipLow))
print("Percentage of high frequency words skipped by skilled readers " + str(monoReaderSkipHi))
print("Total percentage of words skipped by skilled readers: " + str(monoReaderSkipTot))