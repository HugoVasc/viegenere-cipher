import re
from unidecode import unidecode


ENGLISH = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
PORTUGUESE = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def standardize(text):
    text = NONLETTERS_PATTERN.sub('', unidecode(text.upper()))
    return text

def getLetterCount(message):
  message = standardize(message)
  letterCount = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}
  for letter in message:
    if letter in ALPHABET:
      letterCount[letter] += 1
  return letterCount

def getItemAtIndexZero(items):
  return items[0]

def getFrequencyOrder(message):
  letterToFreq = getLetterCount(message)
  freqToLetter = {}
  for letter in ALPHABET:
      if letterToFreq[letter] not in freqToLetter:
        freqToLetter[letterToFreq[letter]] = [letter]
      else:
        freqToLetter[letterToFreq[letter]].append(letter)
  
  for freq in freqToLetter:
    freqToLetter[freq].sort(key=ENGLISH.find, reverse=True)
    freqToLetter[freq] = ''.join(freqToLetter[freq])
  
  freqPairs = list(freqToLetter.items())
  freqPairs.sort(key=getItemAtIndexZero, reverse=True)
  # print('\nFrequência por Letra:\n', freqPairs)
  
  freqOrder = []
  for freqPair in freqPairs:
    freqOrder.append(freqPair[1])

  return ''.join(freqOrder)

def getScore(message:str, Language:str = "EN"):
  freqOrder = getFrequencyOrder(message)

  if(Language != 'PT'):
    AlphabetOrderedByCommonLetters = ENGLISH
  else:
    AlphabetOrderedByCommonLetters = PORTUGUESE


  matchScore = 0

  for commonLetter in AlphabetOrderedByCommonLetters[:6]:
    if commonLetter in freqOrder[:6]:
      matchScore +=1
  for uncommonLetter in AlphabetOrderedByCommonLetters[-6:]:
    if uncommonLetter in freqOrder[-6:]:
      matchScore +=1
  return matchScore

# if __name__ == "__main__":
#     with open ('./desafio1.txt', 'r') as file:
#       text = ''.join(file.readlines())
#     letterCount = getLetterCount(text)
#     print('\nFrequência de cada letra: \n', letterCount)
#     print('\nOrdem de frequencia: ', getFrequencyOrder(text))
#     print('Score: ', getScore(text, 'EN'))
