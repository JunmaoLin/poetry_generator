import nltk
import pronouncing
import random

# This uses the King James Bible as the corpus
# Use: nltk.corpus.gutenberg.fileids()
# to see which other gutenberg works are available.
#pre_my_corpus = nltk.corpus.gutenberg.words('bible-kjv.txt')

# This uses all the words in the entire gutenberg corpus
#pre_my_corpus = nltk.corpus.gutenberg.words()

# This loop constructs a corpus from all the shakespeare plays included in the
# shakespeare corpus included in NLTK
# Use: nltk.corpus.shakespeare.fileids()
# to see which shakespeare works are included.
pre_my_corpus = []
for fid in nltk.corpus.shakespeare.fileids():
    pre_my_corpus += nltk.corpus.shakespeare.words(fid)

my_corpus = []
for w in pre_my_corpus:
    my_corpus.append(w.lower())

bigrams = nltk.bigrams(my_corpus)
cfd = nltk.ConditionalFreqDist(bigrams)

# next_word_generator
# This function...
def next_word_generator(source = None):
    result = None
    #print()
    #print("SOURCE:", source)
    if (source == None) or (source not in cfd) or (not source.isalpha()):
        while result == None or not result.isalpha():
            result = random.choice(my_corpus)
    else: 
        #print("CFD ENTRY:")
        #print(cfd[source])
        init_list = list(cfd[source].elements())
        #print("INIT_LIST:")
        #print(init_list)
        choice_list = [x for x in init_list if x.isalpha()]
        #print("CHOICE_LIST:")
        #print(choice_list)
        #print()
        if len(choice_list) > 0:
            result = random.choice(choice_list)
        else:
            while result == None or not result.isalpha():
                result = random.choice(my_corpus)
    return result


# This function takes a single input:
# word - a string representing a word
# The function returns the number of syllables in word as an
# integer.
# If the return value is 0, then word is not available in the CMU
# dictionary.
def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    count_list = [pronouncing.syllable_count(x) for x in phones]
    if len(count_list) > 0:
        result = max(count_list)
    else:
        result = 0
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of words that rhyme with
# the input word.
def get_rhymes(word):
    result = []
    pre_result = pronouncing.rhymes(word)
    for w in pre_result:
        if w in my_corpus:
            result.append(w)
    #print()
    #print("PRE_RESULT:", len(pre_result))
    #print(pre_result)
    #print("RESULT:", len(result))
    #print(result)
    #print()
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of strings. Each string in the list
# is a sequence of numbers. Each number corresponds to a syllable
# in the word and describes the stress placed on that syllable
# when the word is pronounced.
# A '1' indicates primary stress on the syllable
# A '2' indicates secondary stress on the syllable
# A '0' indicates the syllable is unstressed.
# Each element of the list indicates a different way to pronounce
# the input word.
def get_stresses(word):
    result = pronouncing.stresses_for_word(word)
    return result

# A test function that demonstrates how each of the helper functions included
# in this file work.  You supply a word and it will run each of the above
# functions on that word.
def test():
    keep_going = True
    while keep_going:
        sw = input("Please enter a word (Enter '0' to quit): ")
        if sw == '0':
            keep_going = False
        elif sw == "":
            pass
        else:
            print("Random 5 words following", sw)
            wl = [sw]
            iw = sw
            for i in range(4):
                elements = list(cfd[iw].elements())
                print()
                nw = next_word_generator(iw)
                print("NW:", nw)
                print("COUNT:", elements.count(nw))
                print()
                wl.append(nw)
                iw = nw
            print(" ".join(wl))
            print()
            print("Pronunciations of", sw)
            print(pronouncing.phones_for_word(sw))
            print()
            print("Syllables in", sw)
            print(count_syllables(sw))
            print()
            print("Rhymes for", sw)
            print(get_rhymes(sw))
            print()
            print("Stresses for", sw)
            print(get_stresses(sw))
            print()

# generate_rhyming_line()
# Complete this function so that it returns a list. The list
# must contain two strings of 5 words each. Each string
# corresponds to a line. The two lines you return must rhyme.
def generate_rhyming_lines():
    returnList = []
    lineOne = ""
    lineTwo = ""

    lineOneWord = next_word_generator(None)
    lineOne += lineOneWord 
    for i in range (4):
        lineOneWord = next_word_generator(lineOneWord)
        lineOne += " " + lineOneWord

    listOfRhymes = get_rhymes(lineOneWord) #lineOneWord should contain the last word generated
    while(len(listOfRhymes) == 0 ): #makes sure there are other words that rhymes
        lineOneWord = next_word_generator(None)
        lineOne = ""
        lineOne += lineOneWord 
        for i in range (4):
            lineOneWord = next_word_generator(lineOneWord)
            lineOne += " " + lineOneWord
        listOfRhymes = get_rhymes(lineOneWord) #lineOneWord should contain the last word generated
    

    lineTwoWord = next_word_generator(None)
    lineTwo += lineTwoWord
    for i in range (3):
        lineTwoWord = next_word_generator(lineTwoWord)
        lineTwo += " " + lineTwoWord

    
    lineTwo += " " + listOfRhymes[random.randint(0, len(listOfRhymes)-1)]

    returnList.append(lineOne)
    returnList.append(lineTwo)                           
    return returnList

# generate_10_syllable_lines()
# Complete this function so that it returns a list. The list
# must contain two strings of 10 syllables each. Each string
# corresponds to a line and each line must be composed of words
# whose number of syllables add up to 10 syllables total.
def generate_10_syllable_lines():
    returnList = []
    lineOne = ""
    lineTwo = ""

    lineOneSyllable = 0
    lineTwoSyllable = 0

    lineOne = next_word_generator(None)
    lineTwo = next_word_generator(None)
    while(lineOneSyllable < 10 or lineTwoSyllable < 10):
        if(lineOneSyllable < 10):  
            newWord = next_word_generator(lineOne)
            while(lineOneSyllable + count_syllables(newWord) >= 11):
                newWord = next_word_generator(lineOne)
            lineOne += " " + newWord
            lineOneSyllable += count_syllables(newWord)
        if(lineTwoSyllable < 10):
            newWord = next_word_generator(lineTwo)
            while(lineTwoSyllable + count_syllables(newWord) >= 11):
                newWord = next_word_generator(lineOne)
            lineTwo += " " + newWord
            lineTwoSyllable += count_syllables(newWord)
            
    returnList.append(lineOne)
    returnList.append(lineTwo)
    
    #print("lineOneSyllable: " + str(lineOneSyllable))
    #print("lineTwoSyllable: " + str(lineTwoSyllable))
    
    return returnList


# generate_metered_line()
# Complete this function so that it returns a string. This string
# will be composed of randonly selected words, will contain 10
# syllables, and the rhythm of the line must match the following
# pattern of stresses: 0101010101
def generate_metered_line():
    returnString = ""
    syllableCount = 0;
    stressCount = 0; #count up to 5 sets of 01 // 5 words

    while(syllableCount < 10):
        newWord = next_word_generator(None) #Randomly selected word
        while('01' not in get_stresses(newWord) or count_syllables(newWord) != 2): #to keep things consistent/predictive each word will have 2 syllables
            newWord = next_word_generator(None)
        returnString += newWord + " "
        stressCount += 1
        syllableCount += count_syllables(newWord)

    #print("syllableCount: " + str(syllableCount)) #should return 10
    #print("stressCount: " + str(stressCount)) #should return 5
        
    return returnString

# generate_line()
# Use this function to generate each line of your poem.
# This is where you will implement the rules that govern
# the construction of each line.
# For example:
#     -number of words or syllables in line
#     -stress pattern for line (meter)
#     -last word choice constrained by rhyming pattern
# Add any parameters to this function you need to bring in
# information about how a particular line should be constructed.
    #takes in a String - typeOfLine,
    #either "generate_rhyming_lines" - return an array from generate_rhyming_lines containing 2 lines of 5 words that rhyme on the last word
    #or "generate_10_syllable_lines" - return an array from generate_10_syllable_lines containing 2 lines of 10 syllable string 
    #or "generate_metered_line" - return a string of 5 random words that has stress pattern 0101010101 with 10 syllables in total
    #else generate a line of 5 words - return a string of 5 words
def generate_line(typeOfLine):
    if(typeOfLine == "generate_rhyming_lines"):
        return generate_rhyming_lines()
    elif(typeOfLine == "generate_10_syllable_lines"):
        return generate_10_syllable_lines()
    elif(typeOfLine == "generate_metered_line"):
        return generate_metered_line()
    else:
        newWord = next_word_generator(None)
        newLine = newWord
        for i in range (4):
            newWord = next_word_generator(newWord)
            newLine += " " + newWord
        return newLine

# generate_poem()
# Use this function to construct your poem, line by line.
# This is where you will implement the rules that govern
# the structure of your poem.
# For example:
#     -The total number of lines
#     -How the lines relate to each other (rhyming, syllable counts, etc)
    #generate_poem will be consist of 10 lines
    #there will be 2 sets of rhyming lines - 4 lines
    #4 lines of 10 syllable counts
    #2 lines of 10 syllable counts with pattern of stresses: 0101010101
def generate_poem():
    line = 0
    poem = ""
    for i in range(2):
        arr = generate_line("generate_rhyming_lines")
        poem += arr[0] + "\n"
        poem += arr[1] + "\n"

    for i in range(2):
        arr = generate_line("generate_10_syllable_lines")
        poem += arr[0] + "\n"
        poem += arr[1] + "\n"

    for i in range(2):
        poem += generate_line("generate_metered_line") + "\n"
        
    return poem


if __name__ == "__main__":

#    test()
#    print()
    
#    result1 = generate_rhyming_lines()
#    print("RHYMING LINES:")
#    print(result1)
#    print()

#    result2 = generate_10_syllable_lines()
#    print("10 SYLllABLE LINES:")
#    print(result2)
#    print()

#    result3 = generate_metered_line()
#    print("METERED LINE:")
#    print(result3)
#    print()
    
    my_poem = generate_poem()
    print("A POEM:")
    print(my_poem)
