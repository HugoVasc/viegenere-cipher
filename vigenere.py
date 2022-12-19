from unidecode import unidecode
import re


NONLETTERS_PATTERN = re.compile('[^A-Z]')

def translate(text: str, key: str, mode: str):
  text = standardize(text)
  key = standardize(key)
  result = ''
  for i in range(len(text)):
    if(mode == 'encrypt'):
      x = (ord(text[i]) + ord(key[i%len(key)])) % 26
    else:
      x = (ord(text[i]) - ord(key[i%len(key)]) + 26) % 26
    x += ord('A')
    if(ord(text[i]) != 32):
      result += chr(x)
    else:
      result += ' '
  return result
    
def standardize(text):
    text = NONLETTERS_PATTERN.sub('', unidecode(text.upper()))
    return text

def encryptMessage(key, message):
    return translate(message, key, 'encrypt')


def decryptMessage(key, message):
    return translate(message, key, 'decritp')


if __name__ == "__main__":
  with open ('./desafio1.txt', 'r') as file:
    plainText = ''.join(file.readlines())
  # plainText = input('Enter the text to be encrypted: ')
  key = input('Enter the key: ')
  cipherText = translate(plainText, key, decritp=True)
  print('Encrypted Text: ', cipherText)
  with open ('./textSample_encripted.txt', 'w') as file:
    file.writelines(cipherText)
  