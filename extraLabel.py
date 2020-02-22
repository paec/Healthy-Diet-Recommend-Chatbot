def extraDisLabel(result):
  entity = ""  
  entityname = ""
  dislist = list()
  i = 0
  while i < len(result['wordlist']):
    word = result['wordlist'][i]
    label = result['labellist'][i]
    # print(word)
    if entity=="":
      if "S-" in label:
        entity = label[2:]
        entityname += word
        dislist.append(entityname)
        entityname =""
        entity=""
      elif "B-" in label:
        entity = label[2:]
        entityname+=word
      else:
        pass
    elif entity!="":

      if "E-" in label:
        entityname += word
        dislist.append(entityname)
        entity = ""
        entityname = ""
      elif "I-" in label:
        entityname += word
      else:
        entity = ""
        entityname = ""
        i-=1

    i+=1

  if entity != "":
    pass

  return dislist


if __name__ == '__main__':
  file = open("data.txt","r",encoding="utf8")

  data = file.readlines()

  result = {'wordlist':[],'labellist':[]}

  for d in data:

    word =  d.split("\t")[0]
    label = d.split("\t")[1].strip()

    result['wordlist'].append(word)
    result['labellist'].append(label)


  dislist = extraDisLabel(result)
  print(dislist)