import pandas as pd
import itertools
import json
import spacy
import re


class Combine:
    __project: list = [r"D:\Study\Real Estate\Risk\Risk New\savedrecs ({}).xls".format(num) for num in range(1, 92)]
    __project2: list = [r"D:\Study\Real Estate\Risk\Risk New\Environment\savedrecs ({}).xls".format(num) for num in
                        range(1, 36)]
    __project.append(r"D:\Study\Real Estate\Risk\Risk New\savedrecs.xls")
    __project2.append(r"D:\Study\Real Estate\Risk\Risk New\Environment\savedrecs.xls")

    def combination(self, selfproject: list):
        stores: list = []
        for nums in selfproject:
            stores.append(pd.read_excel(nums))
        return pd.concat(stores, ignore_index=True)

    def inTotal(self):
        anthony = pd.concat([self.combination(self.__project), self.combination(self.__project2)], ignore_index=True)
        kw: pd.DataFrame = anthony["Keywords Plus"]
        lkw: list = kw.str.split("; ").to_list()
        lkw = list(itertools.chain(*lkw))
        with open(r"", "w") as fp:
            json.dump(lkw, fp)
        return lkw

    def fastGeneration(self):
        inall: pd.DataFrame = pd.concat([self.combination(self.__project), self.combination(self.__project2)],
                                        ignore_index=True)
        inall.to_excel(r"D:\Study\Real Estate\Risk\Risk New\Risk_Simplified.xlsx")
        return


class Auxilary:
    __location: str = r""

    def applyFunc(self, args: str):
        args = args.lower()
        position: list = args.split()
        nextpos: int = 0
        for num in range(0, len(position)):
            if "project" in position[num]:
                nextpos = num
                break
        return " ".join(position[nextpos - 1: nextpos + 1]) if nextpos else "Not In list"

    def howMany(self, args: str):
        return True if args.find("project") == -1 else False

    @property
    def napplyFunc(self, args: str):
        """
        this maybe a faster process function... compare with the upper applyFunc one
        :param args: string
        :return: string
        """
        pos: int = args.find("project")
        return args[pos - 25 if len(args) - 25 < 0 else 0: pos + 7] if pos != -1 else "Not In list"


class NLPAnalysis:
    """
    tips: do remember clean out null value then use functions in "apply"
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.Defaults.stop_words |= {"a risk", "some risk", "risk", "risks", "the risk"}
        self.stwords = self.nlp.Defaults.stop_words
        return

    def applyNlp(self, args: str):
        doc = self.nlp(args)
        storage: list = []
        for ent in doc.ents:
            if ent.label_ == "ORG": storage.append([ent.text, ent.label_])
        return storage


def reExp(args: str):
    """
    only need to use regular expression to found out the risk and grab the former two words
    :param args:
    :return:
    """
    nlp = spacy.load("en_core_web_sm")
    risks = re.findall(r"(\w+) [Pp]roject?", args)
    risks = list(set(risks))
    stword = nlp.Defaults.stop_words
    risks = [words + " project" if words not in stword else None for words in risks]
    return list(filter(lambda x: x is not None, risks))


files, inall = [], []


def recognize(args: str, nlp):
    partial: list = []
    doc = nlp(args)
    for ent in doc.ents:
        if ent.label_ == "ORG": partial.append([ent.text, ent.label_])
    return partial


def policy():
    for ele in files:
        nlp = spacy.load("en_core_web_sm")
        inall.append(ele.apply(recognize, args=(nlp,)))
        del nlp


if __name__ == "__main__":
    print("system initializing...")
    jack = NLPAnalysis()
    file = pd.read_excel(r"D:\Study\Real Estate\Risk\Risk New\Risk_Simplified.xlsx")
    abst: pd.DataFrame = file.Abstract[0:100].dropna(how="any")
    abst.apply(reExp("project"))
