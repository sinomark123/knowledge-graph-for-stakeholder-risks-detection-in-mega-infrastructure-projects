# for val in self.obj:
#     if val == "0" or not val:
#         continue

#     res = re.split(sentence_pattern, val, maxsplit=1)

#     tuples = ("", "", "")
#     one_risk = True

#     for string in res:
#         string = string.strip()

#         if "risk" in string.split(" ")[-1]:
#             if string not in risk_pool:
#                 risk_pool.add(string)
#                 tuples = (string, "", "")

#         elif "risk" not in string.split(" ")[-1]:
#             if len(string.split(" ")) > 4:
#                 tuples = (tuples[0], string, "")
#             elif string not in type_pool:
#                 tuples = (tuples[0], tuples[1], string)
#                 type_pool.add(string)
    
#     str_storage.append(tuples)