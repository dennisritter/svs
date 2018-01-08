import math
# Key length -> bit
keyLens = [40, 56, 64, 112, 128]
# calcs/second
asicSpeed = 5 * 10**8
# how much $$ do we have
money = 1000000
# integration cost/unit
integrationCost = 50
# asic cost/unit
asicCost = 50

#####
# how many asics do we have?
print('##### ASICS #####')
asicsNum = money / (asicCost + integrationCost)
print('we got enough money for ', asicsNum, ' asics.')

print('##### BRUTEFORCE TIMES #####')
for keyLen in keyLens:
  maxP = 2**(keyLen)
  avgP = 2**(keyLen-1)
  minTime = 1/(asicSpeed*asicsNum)
  avgTime =  avgP / (asicSpeed*asicsNum)
  maxTime =  maxP / (asicSpeed*asicsNum)
  print(keyLen, 1, avgTime, maxTime)

print('##### BRUTEFORCE TIMES - MOORES LAW #####')
money = 1000000000
asicsNum = money / (asicCost + integrationCost)
results = []
def calcMoore(keyLen, years):

    avgP = 2**(keyLen-1)
    avgTime = avgP / (asicSpeed * asicsNum * 2**years)
    if (avgTime / 3600 <= 24.0):
      print("**** GOT ONE ****")
      return [keyLen, avgTime / 3600, years]
    else:
      return(calcMoore(keyLen, years+1))

for keyLen in keyLens:
  results.append(calcMoore(keyLen, 0))

print(results)
