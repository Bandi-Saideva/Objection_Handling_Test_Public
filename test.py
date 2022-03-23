# https://notebooks.outplayhq.com/user/admin/notebooks/shared/objection-handling/regex-based-engine/Regex-engine-validation-Saideva-Copy.ipynb
# follow above link for more descriptive notebook
# import re
import pandas as pd
import ast

data = pd.read_csv("msg_with_label_and_regexResults")
# print(ast.literal_eval(df.iloc[0]["label"])[0]["labels"][0])

## RECALL

data1 = data
print(data1.shape)
objections = [ "Authority", "Not Interested", "Interested", "Budget", "Timing", "Competitor"]
recall_df = pd.DataFrame(columns = ['Objection', "total_count", "true_positive_count", "recall"])
for objection in objections:
    true_positive_count = 0
    total = 0
    for index, row in data1.iterrows():
        for dic in ast.literal_eval(row["label"]):
            if dic["labels"][0] == objection:
                total += 1
                for regex_dic in ast.literal_eval(row["regex_results"]):
                    if (regex_dic["class"]==objection) and (dic["text"].find(regex_dic["evidence"]) != -1 or regex_dic["evidence"].find(dic["text"]) != -1):
                        true_positive_count += 1
    recall_df.loc[len(recall_df)] = [objection, total, true_positive_count, true_positive_count/total]
recall_df.sort_values(by=['recall'], ascending=False, inplace = True)

total_recall = (recall_df["true_positive_count"].sum() / recall_df["total_count"].sum())
print(total_recall)

## PRECISION

data1 = data
objections = [ "Authority", "Not Interested", "Interested", "Budget", "Timing", "Competitor"]
precison_df = pd.DataFrame(columns = ['Objection', "total_count", "true_positive_count", "precison"])
for objection in objections:
    true_positive_count = 0
    total = 0
    for index, row in data1.iterrows():
        for regex_dic in ast.literal_eval(row["regex_results"]):
            if regex_dic["class"] == objection:
                total += 1
                for dic in ast.literal_eval(row["label"]):
                    if dic["labels"][0] == objection and (dic["text"].find(regex_dic["evidence"]) != -1 or regex_dic["evidence"].find(dic["text"]) != -1):
                        true_positive_count += 1
                        break
    precison_df.loc[len(precison_df)] = [objection, total, true_positive_count, true_positive_count/total]
precison_df.sort_values(by=['precison'], ascending=False, inplace = True)

total_precison = precison_df["true_positive_count"].sum() / precison_df["total_count"].sum()
print(total_precison)

## F1 SCORE

f1_score = (2 * total_precison * total_recall) / (total_recall + total_precison)
print(f1_score)
    
print(f"\nPrecision: {total_precison}, Recall: {total_recall} and F1 Score: {f1_score}.")

TP = 0
FN = 0
for objection in objections:
    for index, row in data1.iterrows():
        for dic in ast.literal_eval(row["label"]):
            if dic["labels"][0] == objection:
                total += 1
                found = 0
                for regex_dic in ast.literal_eval(row["regex_results"]):
                    if (regex_dic["class"]==objection) and (dic["text"].find(regex_dic["evidence"]) != -1 or regex_dic["evidence"].find(dic["text"]) != -1):
                        TP += 1
                        found = 1
                if found == 0:
                    FN += 1

TP = 0
FP = 0
total = 0
for objection in objections:
    for index, row in data1.iterrows():
         for regex_dic in ast.literal_eval(row["regex_results"]):
            if regex_dic["class"] == objection:
                total += 1
                found = 0
                for dic in ast.literal_eval(row["label"]):
                    if dic["labels"][0] == objection and (dic["text"].find(regex_dic["evidence"]) != -1 or regex_dic["evidence"].find(dic["text"]) != -1):
                        TP += 1
                        found = 1
                if found == 0:
                    FP += 1 
TN = 0                  
for objection in objections:
    for index, row in data1.iterrows():
        for dic in ast.literal_eval(row["label"]):
            if dic["labels"][0] != objection:
                total += 1
                found = 0
                for regex_dic in ast.literal_eval(row["regex_results"]):
                    if (regex_dic["class"]==objection) and (dic["text"].find(regex_dic["evidence"]) != -1 or regex_dic["evidence"].find(dic["text"]) != -1):
                        found = 1
                if found == 0:
                    TN += 1
                    
                    
with open('metrics.txt', 'w') as outfile:
    outfile.write(f"\nPrecision: {total_precison}, Recall: {total_recall} and F1 Score: {f1_score}.")
    outfile.write(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}.")
