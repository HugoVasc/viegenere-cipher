from unidecode import unidecode

def viegenereCipher(text, key):
  text = normalize(text)
  key = normalize(key)
  cipher = ''
  for i in range(len(text)):
    if(ord(text[i]) != 32):
      x = (ord(text[i]) + ord(key[i%len(key)])) % 26
      x += ord('A')
      cipher += chr(x)
    else:
      cipher += ' '
  return cipher
  
def viegenereDecipher(cipher, key):
  key = normalize(key)
  text = ''
  for i in range(len(cipher)):
    if(ord(cipher[i]) != 32):
      x = (ord(cipher[i]) - ord(key[i%len(key)]) + 26) % 26
      x += ord('A')
      text += chr(x)
    else:
      text += ' '
  return text

def normalize(text):
    text = text.upper()
    text = unidecode(text)
    return text

if __name__ == "__main__":
  plainText = input('Enter the text to be encrypted: ')
  key = input('Enter the key: ')
  cipherText = viegenereCipher(plainText, key)
  print('Encrypted Text: ', cipherText)
  plainText = viegenereDecipher(cipherText, key)
  print('Decrypted Text: ', plainText)