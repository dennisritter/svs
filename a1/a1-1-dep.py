import enchant
import copy

def getPattern(word):
  pattern = []
  for c in word:
    pattern.append(list(pos for pos, char in enumerate(word) if char == c))

  return pattern

def compareWordPattern(word, dictWord):
  wp = getPattern(word)
  #print("[PATTERN] ", wp)
  dwp = getPattern(dictWord)
  return wp == dwp

def compareWordLists(wordsA, wordsB):
  return

def filterWords(word):
    word_l = len(word)
    possible_words = list(dCount[str(word_l)]);

    for dw in dCount[str(word_l)]:
      if (compareWordPattern(word, dw) == False):
        possible_words.remove(dw)
    #print('[RESULT] ', word, '-->', possible_words)
    #if (possible_words.len == 1):
    return possible_words

##########
def prepare(string):
  enc = "xureveoulrefknpavberweqwuegwceappergvleovlrazfbevdfaewmedfbwubjvbyenpfalusfeabdensavlvbyenavbecalexwsbeabdevecvppeyvtfeqwueaejwonpfrfeajjwubrewmergfelqlrfoeabdefknwubdergfeajruaperfajgvbylewmergfeysfarefknpwsfsewmergfersurgergfeoalrfsexuvpdfsewmeguoabegannvbfll"
  enchd = enchant.Dict("en_US")

  ### Prepare Dictionary
  words = open("10k.txt", "r").readlines()
  d = []
  for w in words:
    # remove \n
    w = w.replace(w[-1:], "")
    # Add to normal words list
    d.append(w)
    # Create Dict to seperate words length
    wc = len(w)
    wcStr = str(wc)
    if wcStr in dCount:
      dCount[wcStr].append(w)
    else:
      dCount[wcStr] = [w]
  # print(dCount)


  # Replace "e" with " ", get words
  enc = enc.replace("e", " ")
  ### Prepare List of encrypted words sorted by length
  enc_words = enc.split(" ")
  enc_words.sort(key = len)
  enc_words = list(reversed(enc_words))

  dec_words = []
  for word in enc_words:
    #if(len(word) > 4):
      before = len(dCount[str(len(word))]);
      after = filterWords(word);
      #print "[LENGTH] ", len(word), "[START] ", before, " [END] ", len(after)
      dec_words.append(after)
        #print(word, after)

  #print(dec_words)
  return [enc_words, dec_words]



enc = "xureveoulrefknpavberweqwuegwceappergvleovlrazfbevdfaewmedfbwubjvbyenpfalusfeabdensavlvbyenavbecalexwsbeabdevecvppeyvtfeqwueaejwonpfrfeajjwubrewmergfelqlrfoeabdefknwubdergfeajruaperfajgvbylewmergfeysfarefknpwsfsewmergfersurgergfeoalrfsexuvpdfsewmeguoabegannvbfll"
dCount = {};
saveChars = {}
tempChars = {}
prepared = prepare(enc)
encWords = prepared[0];
decWords = prepared[1];
print(enc)
print(encWords)

def getTempChars(enc, dec):
  # Copy Dictionary containing save key letters
  #tempChars = dict(saveChars)
  tempChars = dict()
  # For each character in words
  for charIndex in range(len(enc)):
    # if Char is not in tempChars already (tho also not in saveChars)
    if(enc[charIndex] not in tempChars):
      # Add char-key and value to tempChars dictionary
      tempChars[enc[charIndex]] = dec[charIndex]
      #print tempChars
  return tempChars

def validateChars(encWord, decWord, decWordsCopy, tempChars):

  #tempDecWords = copy.deepcopy(decWords)

  for keyChar in tempChars:
    if (keyChar in saveChars and keyChar in encWord):
      tempChars = dict(tempChars.items() + saveChars.items())
      encCharPattern = list(pos for pos, char in enumerate(encWord) if char == keyChar)
      decCharPattern = list(pos for pos, char in enumerate(decWord) if char == saveChars[keyChar])
      #print('[SAVE ENC PATTERN]', keyChar, encWord, encCharPattern)
      #print('[SAVE DEC PATTERN]', saveChars[keyChar], decWord, decCharPattern)
      if(encCharPattern != decCharPattern):
        #print('[FALSE PATTERN]')
        #print(saveChars)
        #print('[SAVE ENC PATTERN]', keyChar, encWord, encCharPattern)
        #print('[SAVE DEC PATTERN]', saveChars[keyChar], decWord, decCharPattern)
        return False;

    for wordIndex in range(len(encWords[:(len(decWords))])):
      #print('########## [SAVETEST PASSED] ##########')
      word = encWords[wordIndex]
      #tempDecWords = list(decWordsCopy[wordIndex])
      #tempDecWordList = tempDecWords[wordIndex]
      tempDecWordList = list(decWordsCopy[wordIndex])
      #if(word.count(keyChar) > 0):
      encCharPattern = list(pos for pos, char in enumerate(word) if char == keyChar)
        #print('[CHECK MAPPING FOR]', word)
      for tempDecWord in tempDecWordList:
        decCharPattern = list(pos for pos, char in enumerate(tempDecWord) if char == tempChars[keyChar])
        if(encCharPattern != decCharPattern):
          tempDecWordList.remove(tempDecWord)
          if(len(tempDecWordList) == 0):
            return False
          #### TO DELETE
          #print('[CHECKING]', tempDecWord)
          #if(tempDecWord.count(tempChars[keyChar]) == 0):
           # tempDecWordList.remove(tempDecWord)
            #print('[CHAR NOT PRESENT] ' + keyChar + ':' + tempChars[keyChar] + ' IN ' + tempDecWord)
            #print('[REMOVE TEMP] ', tempDecWord)
            #if(len(tempDecWordList) == 0):
              #print('[REMOVE] ', decWord)
             # return False
  return True

# For wordlists in possible decrypted words..

for wordListIndex in range(len(decWords)):
  encWord = encWords[wordListIndex]
  # For each word in the list of possible words..
  decWordsLen = len(decWords[wordListIndex])
  decWordsCopy = copy.deepcopy(decWords)
  if(wordListIndex > 0):
    print(decWords[wordListIndex-1])
    if(len(decWords[wordListIndex-1]) == 1):
      #print(wordListIndex - 1, encWords[wordListIndex - 1], decWords[wordListIndex - 1])
      #print(getTempChars(encWords[wordListIndex - 1], decWords[wordListIndex - 1][0]), encWords[wordListIndex - 1], decWords[wordListIndex - 1][0])
      saveChars = dict(getTempChars(encWords[wordListIndex - 1], decWords[wordListIndex - 1][0]).items() + saveChars.items());
      #print(saveChars, encWords[wordListIndex - 1], decWords[wordListIndex - 1][0])
      #saveChars = dict(getTempChars(encWords[wordListIndex - 1], decWords[wordListIndex - 1][0] ).items() + saveChars.items())
      #print(saveChars)

  for i in range(decWordsLen):
    decWord = decWordsCopy[wordListIndex][i]
    #print('[VALIDATING] ', decWord)
    tempChars = getTempChars(encWord, decWord)
    #tempChars = dict(getTempChars(encWord, decWord).items() + saveChars.items())
    #print(tempChars, encWord, decWord)
    #print(getTempChars(encWord, decWord), encWord, decWord)
    if(validateChars(encWord, decWord, decWordsCopy, tempChars) == False):
      #print('#################################')
      #print('[FALSE MAPPING] ', decWord)
      #print('#################################')
      decWords[wordListIndex].remove(decWord)

    #else:
     # if(len(decWords[wordListIndex]) == 1):
      #  saveChars = dict(tempChars)
       # print(saveChars)
    #print(decWords[wordListIndex])
print(decWords)
print(encWords)
print(saveChars)


