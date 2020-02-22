import re
import prettytable as pt

tb = pt.PrettyTable()
tb2 = pt.PrettyTable()
tb.field_names = ['','Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O']
tb2.field_names = ['','Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O']
tb.float_format = ".5"

true_pos = dict()
true_neg = dict()
false_pos = dict()
false_neg = dict()

true_pos = true_pos.fromkeys(['Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O'],0)
true_neg = true_neg.fromkeys(['Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O'],0)
false_pos = false_pos.fromkeys(['Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O'],0)
false_neg = false_neg.fromkeys(['Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O'],0)

true = 0
false = 0
true_entity = 0
false_entity = 0

def divide(x,y):
    return x / y if y else float(0)


file = open("lstm_result_test.txt","r",encoding="utf8") 

data = file.readlines()

count = 0 

entity_end = False
totalcorrect = True

for d in data:

    count+=1

    if d.strip() == '':
        continue

    result = d.split()

    token = result[0]
    answer = result[1]
    predict = result[2]

    if answer == "O" or re.match(r"^B-.+",answer) or re.match(r"^S-.+",answer):
        entity_end = True


    answer_match = re.match(r"[A-Z]-([A-Za-z]+)", answer)
    predict_match = re.match(r"[A-Z]-([A-Za-z]+)", predict)

    if answer_match :
        answer_type = answer_match.group(1)
    else:
        answer_type  = "O"

    if predict_match :
        predict_type = predict_match.group(1)
    else:
        predict_type = "O"

    if answer == predict:
        true+=1
        true_pos[predict_type] += 1

    else:
        # print(token)
        # print("answer: ",answer," predict",predict)
        # print("---------------------------------------")
        totalcorrect = False
        false+=1
        false_pos[predict_type] += 1
        false_neg[answer_type] += 1

    if entity_end:

        if totalcorrect:
            true_entity  +=1
        else:
            false_entity +=1

        totalcorrect = True
        entity_end = False



precision = dict()
recall = dict()
f1_score = dict()

for label in ['Tim','Org','Sym','Exa','Abb','Dep','Dis','Tre','Med','Hea','O']:
    precision[label] = divide(true_pos[label],(true_pos[label]+false_pos[label]))
    recall[label] = divide(true_pos[label],(true_pos[label]+false_neg[label]))
    f1_score[label] = divide(2 * precision[label] * recall[label] , (precision[label]+recall[label]))


tb.add_row(["Precision",precision['Tim'],precision['Org'],precision['Sym'],precision['Exa'],precision['Abb'],precision['Dep'],precision['Dis'],precision['Tre'],precision['Med'],precision['Hea'],precision['O']])
tb.add_row(["---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',])
tb.add_row(["Recall",recall['Tim'],recall['Org'],recall['Sym'],recall['Exa'],recall['Abb'],recall['Dep'],recall['Dis'],recall['Tre'],recall['Med'],recall['Hea'],recall['O']])
tb.add_row(["---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',])
tb.add_row(["F1-score",f1_score['Tim'],f1_score['Org'],f1_score['Sym'],f1_score['Exa'],f1_score['Abb'],f1_score['Dep'],f1_score['Dis'],f1_score['Tre'],f1_score['Med'],f1_score['Hea'],f1_score['O']])


tb2.add_row(["True positive",true_pos['Tim'],true_pos['Org'],true_pos['Sym'],true_pos['Exa'],true_pos['Abb'],true_pos['Dep'],true_pos['Dis'],true_pos['Tre'],true_pos['Med'],true_pos['Hea'],true_pos['O']])
tb2.add_row(["---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',])
tb2.add_row(["false positive",false_pos['Tim'],false_pos['Org'],false_pos['Sym'],false_pos['Exa'],false_pos['Abb'],false_pos['Dep'],false_pos['Dis'],false_pos['Tre'],false_pos['Med'],false_pos['Hea'],false_pos['O']])
tb2.add_row(["---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',"---------",'---------', '---------', '---------',])
tb2.add_row(["false negative",false_neg['Tim'],false_neg['Org'],false_neg['Sym'],false_neg['Exa'],false_neg['Abb'],false_neg['Dep'],false_neg['Dis'],false_neg['Tre'],false_neg['Med'],false_neg['Hea'],false_neg['O']])


print(tb)
print(tb2)
print("\nword-level accuracy: ",divide(true,true+false) )
print(      "total word: " , true+false , "  true word: ", true)

print("\nentity-level accuracy: ",divide(true_entity,true_entity+false_entity) )
print(      "total enetity: " , true_entity+false_entity , "  true entity: ", true_entity)

# exit()

resultfile = open("lstm_result_test_eval.txt","w",encoding="utf8")

resultfile.write(str(tb))
resultfile.write("\n")
resultfile.write(str(tb2))
resultfile.write("\n")
resultfile.write("\nword-level accuracy: "+str(divide(true,true+false) )+"\n")
resultfile.write(      "total word: " + str(true+false) + "  true word: "+ str(true)+"\n")
resultfile.write("\nentity-level accuracy: "+str(divide(true_entity,true_entity+false_entity) )+"\n")
resultfile.write(      "total enetity: " + str(true_entity+false_entity) + "  true entity: "+ str(true_entity))