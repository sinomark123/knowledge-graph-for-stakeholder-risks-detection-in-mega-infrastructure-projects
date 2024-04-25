from fpgrowth_py import fpgrowth
import pandas as pd
import re
import json
import spacy

project = r"D:\Study\Real Estate\Project\Gg.csv"
risk = r"D:\Study\Real Estate\Risk\Risk New\Risk_Simplified.xlsx"
stake = r"D:\Study\Real Estate\StakeHolder\expansive.csv"

project1 = r"D:\Code Working Area\Python\knowledge-graph-for-stakeholder-risks-detection-in-mega-infrastructure-projects\ExcelData\newTitle_Project.xlsx"
risk0 = r"D:\Code Working Area\Python\knowledge-graph-for-stakeholder-risks-detection-in-mega-infrastructure-projects\ExcelData\RiskFinal.xlsx"
stake1 = r"D:\Code Working Area\Python\knowledge-graph-for-stakeholder-risks-detection-in-mega-infrastructure-projects\ExcelData\New_StakeHolder_Abstract.xlsx"

pj = pd.read_csv(project, sep = ",")
risk1 = pd.read_excel(risk)
stk = pd.read_csv(stake, sep = ",")

prj = pd.read_excel(project1)
risk2 = pd.read_excel(risk0)
stk1 = pd.read_excel(stake1)

en = spacy.load('en_core_web_sm')
stopwords = en.Defaults.stop_words

# get the target text from original dataset to match
nproject = pd.DataFrame(pj["Article Title"])
nrisk = pd.DataFrame(risk1["Abstract"])
nstack = pd.DataFrame(stk["Abstract"])


# pre-process of matching

def reduction(args: pd.Series, val: str):
    args = str(args)
    #     variables = "\b" + args + "\b"
    return re.search(rf"\b{args}\b", val) != None


def match_attributes(args: str):
    res = prj["Article Title"].astype(str).apply(reduction, args=(args,))
    casualty = prj["Article Title"][res == True].to_list()
    res = risk2["Abstract"].apply(reduction, args=(args,))
    casualty = [*casualty, *risk2.Abstract[res == True].to_list()]
    res = stk1.name.apply(reduction, args=(args,))
    casualty = [*casualty, *stk1.name[res == True].to_list()]
    return casualty


for value in nrisk[1:50].itertuples():
    if type(value.Abstract) is int or type(value.Abstract) is float:
        print(value)
        continue
    print(match_attributes(value.Abstract), "\n")