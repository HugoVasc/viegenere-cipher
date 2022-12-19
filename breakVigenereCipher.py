import itertools
import re

from unidecode import unidecode


from freqAnalysis import getScore, standardize
from vigenere import decryptMessage

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False # Modo silencioso, não imprime nada na tela
NUM_MOST_FREQ_LETTERS = 4 # Máximo de letras para cada subchave
MAX_KEY_LENGTH = 16 # Tamanho máximo da chave a ser testada
NONLETTERS_PATTERN = re.compile('[^A-Z]')
#Pontuação de 1 a 12 de similaridade com a frequência de letras de um texto em inglês
SCORE_THRESHOLD = 8
LANGUAGE = 'PT'


DESAFIO2 = """tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."""

freqPort = {'A':15, 'B':1, 'C':4, 'D':5, 'E':13, 'F':1, 'G':1, 'H':1, 'I':6, 'J':0, 'K':0, 'L':3, 'M':5, 'N':5, 'O':11, 'P':3, 'Q':1, 'R':7, 'S':8, 'T':4, 'U':5, 'V':2, 'W':0, 'X':0, 'Y':0, 'Z':0}
freqEng = {'A':8, 'B':2, 'C':5, 'D':3, 'E':11, 'F':2, 'G':2, 'H':3, 'I':8, 'J':0, 'K':1, 'L':5, 'M':3, 'N':7, 'O':7, 'P':3, 'Q':0, 'R':8, 'S':6, 'T':7, 'U':4, 'V':1, 'W':1, 'X':0, 'Y':2, 'Z':0}

def main():
    # with open ('./desafio1.txt', 'r') as file: ciphertext = ''.join(file.readlines())
    ciphertext = DESAFIO2
    
    print("Mensagem decifrada:",hackVigenere(ciphertext))


def findRepeatSequencesSpacings(message):
    #Verifica a repetição de sequências de 3 a 5 letras no texto cifrado
    #Retorna um dicionário com as chaves das sequências e os valores de 
    #uma lista de espaçamentos (número de letras entre as repetições)

    # Remove os caracteres que não são letras:
    message = NONLETTERS_PATTERN.sub('', message.upper())

    seqSpacings = {}
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] 
            
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
   #Obtem os fatores úteis para um possível tamanho de chave,
   #maiores que 1 e menores que MAX_KEY_LENGTH

    if num < 2:
        return [] # Ignora fatores menores que 2.

    factors = [] # Lista de fatores úteis


    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # Remove fatores duplicados.


def getItemAtIndexOne(items):
    return items[1]


def getMostCommonFactors(seqFactors):
    # Obtem os fatores mais comuns de uma lista de sequências e espaçamentos
    factorCounts = {} # Dicionario cuja chave é um fator e o 
    # valor é a quantidade de vezes que ele aparece

    # seqFactors te um formato semelhante a: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH: # Ignora fatores maiores que MAX_KEY_LENGTH   
            factorsByCount.append( (factor, factorCounts[factor]) )

    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ciphertext):
    # Busca sequencias de 3 a 5 letras repetidas que se repetem ao 
    # longo do texto cifrado e obtem os espaçamentos entre elas
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    factorsByCount = getMostCommonFactors(seqFactors)

    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    print('\n', '----- Tamanhos de Chave Prováveis -----', '\n', allLikelyKeyLengths)
    return allLikelyKeyLengths

def getNthSubkeysLetters(nth, keyLength, message):
    # Retorna uma string com todas as letras que são a N-ésima
    # letra do texto cifrado a cada tamanho de chave.
    # Ex. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    message = standardize(message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determina as letras mais prováveis para cada letra da chave
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertext)

        # freqScores é uma lista de tuplas (chave, pontuação)
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, getScore(decryptedText, LANGUAGE))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=getItemAtIndexOne, reverse=True) # Ordena por pontuação decrescente

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # Use i + 1 so the first letter is not called the "0th" letter:
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()

    # Testa todas as combinações de letras mais prováveis para cada letra da chave
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = decryptMessage(possibleKey, ciphertext)

        # retorna o texto decifrado se a pontuação for maior que o SCORE_THRESHOLD
        if getScore(decryptedText, LANGUAGE) >= SCORE_THRESHOLD:
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:50]) # Only show first 50 characters.
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    return None   

def hackVigenere(ciphertext: str):
    ciphertext = unidecode(ciphertext.upper())
    
    # Utiliza o método de Kasiski Examination para determinar os tamanhos de chave mais prováveis
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        #Testa todas as combinações de letras mais prováveis para cada letra da chave, para diversos tamanhos de chave
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    if hackedMessage == None:
            print('Não foi possível decifrar o texto com os tamanhos de chave prováveis obtidos com o método de Kasiski.')
    return hackedMessage

if __name__ == '__main__':
    main()