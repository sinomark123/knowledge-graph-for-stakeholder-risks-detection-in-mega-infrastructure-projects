from typing import *
import re
from collections import Counter

INTERTIAL_vocabulary = ["sure", "I'd be happy", "happy", "please", "help", "given sentence", \
                        "I", "let", "based", "here are", "understood", "predictions", "mentioned", \
                            "sentence"]
escape_vocabulary=[re.escape(word) for word in INTERTIAL_vocabulary]
pattern = rf"\b({'|'.join(escape_vocabulary)})\b"

# Input Example
"""
[  
Understood! Here are my predictions for each element mentioned in the sentence:
* Project: Electricity generation sector
Risk: Increased emissions through offsets
Stakeholders: Host countries, project developers, investors
0
]
"""

class Answer:
    
    rawdata: str=""
    listdata: List[str]=[]

    prefix=["*", *[str(num)+"." for num in range(20)]]
    delete="*"


    def __init__(self, block) -> None:
        self.rawdata=block
        

    def validate(self):
        if not self.rawdata or isinstance(self.rawdata, List[str]):
            print("invalidate None block input. Please check your input.")
            raise ValueError(f"input {self.rawdata}")
    
    def inner_calling(self):
        self.rawdata=[]


    @staticmethod
    def sys_clean(string):
        matches = re.search(pattern, string, flags=re.IGNORECASE)
        return  "0"  if matches else string

    def prefix_clean(self, string):
        pattern = r"\* |\d+\.\s"
        matches = re.sub(pattern=pattern, repl='', string=string, flags=re.MULTILINE)
        return matches

    def prefix_count(self, string: str) -> bool:
        string = [val.lower().strip() for val in string.split(" ", -1)]
        # if len(string)<2: return ""

        RISK=Counter(["risk", "risks", "risk:", "risks:"] + [str(num) for num in range(1, 10)])
        RISK_TYPE=Counter(["risk", "risks","of", "type", "type:", "types"])

        target=Counter(string)
        
        TYPE_SOCRE = sum((target&RISK_TYPE).values()) / len(target)
        RISK_SCORE = sum((target&RISK).values()) / len(target)

        if TYPE_SOCRE > 0.5 or RISK_SCORE>0.5:
            return True

        return False

    def head_off(self, tar: str):
        integrate = tar.split(":", 1)

        if len(integrate)<2: return tar

        head, body = integrate[0], integrate[1:]
        if self.prefix_count(head): 
            return " ".join(body) if body else None
        
        return tar


    def parse(self): 

        self.listdata = [cnt.strip() for cnt in self.rawdata.split("\n")]

        for index, val in enumerate(self.listdata):
            first = self.sys_clean(val)
            second = self.prefix_clean(first)
            self.listdata[index] = self.head_off(second)

        return self.listdata
    
# start from here, we need to divide words to three type:
# qualifed risk
# qualifed risk_type
# not qualifed answer

class ShortSentenceCut(Answer):
    """
    Parse the main function to process text.
    After parsing, the text is expected to be divided into four types:
    - risk_properly_labeled: risk well-identified and classified
    - risk_type_properly_labeled: risk type well-identified
    - risk_secondry_process: risk too long and hard to be summarized
    - risk_type_secondry_process: unexpected labeling result

    Phrase one: only need to clean the text
    """

    class Risks:
        ...

    class RiskType:
        ...

    def __init__(self, block):
        super().__init__(block)
        self.obj = super().parse()
        while self.obj and (self.obj[0] == "" or self.obj[0] == "0"):
            self.obj.pop(0)
        while self.obj and (self.obj[-1] == "" or self.obj[-1] == "0"):
            self.obj.pop()
        
        for index, val in enumerate(self.obj): 
            if val == '0': del self.obj[index]


    def __clean__(self):
        for index, val in enumerate(self.obj):
            if not val or val=="0": del self.obj[index]

    def risk_wrap(self, query: List):
        ...

    def risk_type(self, query: List):
        ...
  
    def input_structure(self, given: List[str]=None):
        """
        Used to split the "risk" and "risk type" and distinct answer shape; usually it includes
        1. risk, risk type are will divided by three " "
        2. one risk followed by one risk type
        3. only have risk or risk type
        4. Disjointed and jumbled answer

        Args:
            given (List[str], optional): The input list of strings. Defaults to None.

        Returns:
            tuple: A tuple containing the following information:
                - forend (bool): Indicates if the given structure is suit for first scenoiro.
                - is_empty (bool): Indicates if the number of " " in list is less than 3.
                - index_e (int): The index of the end point of risk.
                - index_s (int): The index of the initial cutting point of risk type.
        """

        given = self.obj if not given else given

        index_e, index_s, forend = len(given), 0, True

        empty_counter = 0

        for index, val in enumerate(given):
            if not val and index+1<len(given):
                if not given[index+1] and given[index-1] and given[index-1]!='0': 
                    index_e=index
                if given[index+1] and not given[index-1]:
                    index_s=index+1
            if not val:
                empty_counter+=1 

        if index_e==len(given) and index_s == 0: forend=False

        return forend, empty_counter<3, index_e, index_s
    
    def format_tracking(self, tracker: List[str] = None) -> List[set]:
        tracker = self.obj if not tracker else tracker

        trigger_s, trigger_e = [0, 1, 2], [val for val in range(len(tracker)-3, len(tracker))]
        inside,  anomaly = False, list()


        for idx, val in enumerate(tracker):
            if (idx in trigger_e or idx in trigger_s) and (val == '0' or not val):
                continue

            if not val: inside = True

        if inside: 
            anomaly.append(tracker)
            return not inside, anomaly


        value, explain = set(), set()

        for idx, val in enumerate(tracker):
            if val == '0' or not val: continue
            if not idx % 2: value.add(val)
            else: explain.add(val)

        return not inside, [value, explain]

    @overload
    def two_group(self) -> List[str]:
        risk_pool: set(str) = set()

        sentence_pattern = r"[^a-zA-Z\s,';]+"
    
        for val in self.obj:
            val = re.split(sentence_pattern, val, maxsplit=1)
            for enu in val:
                val = enu.strip()
                if enu == "0" or not enu or "risk" not in enu.split(" ")[-1]: 
                    continue

                if enu not in risk_pool:
                    risk_pool.add(enu)

        return list(risk_pool)       

    @staticmethod
    def match_lists(list1, list2):
        matched_tuples = []

        list1, list2 = list(list1), list(list2)

        for element1, element2 in zip(list1, list2):
            matched_tuples.append((element1, element2))

        # If the lists have different lengths, handle the remaining elements
        remaining_length = abs(len(list1) - len(list2))
        if remaining_length > 0:
            if len(list1) > len(list2):
                remaining_elements = list1[-remaining_length:]
                matched_tuples.extend([(element, 0) for element in remaining_elements])
            else:
                remaining_elements = list2[-remaining_length:]
                matched_tuples.extend([(0, element) for element in remaining_elements])

        return matched_tuples
    
    @staticmethod
    def str_clear(strlist: List[str]):
        return [val for val in strlist if val or val!='0']

    def two_group(self) -> Tuple[List[str], List[Tuple[str, str, str]]]:
        """
        Refined by ChatGPT, still need more development stages
        """
        sentence_pattern = r"[^a-zA-Z\s,';]+"

        str_storage: dict = {
            "anomaly": [],
            "normal": {
                "compose": []
            }

        }
        risk_pool: Set[str] = set()
        type_pool: Set[str] = set()

        accept, empty, te, ts = self.input_structure()

        if empty: self.obj = [val for val in self.obj if val]

        if not accept and (not len(self.obj) % 2 and empty): 
            goddammn, tracing = self.format_tracking()

            if not goddammn: 
                str_storage["anomaly"].append(tracing)
                return str_storage
            else: 
                valid_val, valid_type = tracing

        elif empty:
            valid_val, valid_type = self.obj, [0]

        else:
            valid_val, valid_type = self.str_clear(self.obj[:te]), self.str_clear(self.obj[ts:])
        str_storage["normal"]["compose"] = [*str_storage["normal"]["compose"], *self.match_lists(valid_val, valid_type)]

        return str_storage   