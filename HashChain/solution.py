import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain. 
seed = "923" #id
target = "30aa442a68a2c4d23786cd4f0bb68f0e"

#this will find the 5th hash in the hashchain. This would be the correct response if prompted with the 6th hash in the hashchain
hashc = seed
previous = ''
while hashc != target:
  previous = hashc
  hashc = md5.new(hashc).hexdigest()
  
print previous #Submit this
print hashc
