import pandas as pd

x = pd.ExcelFile("evaluation tool.xlsm")
s = x.sheet_names[1]
p = x.parse(s)
t= p.drop(p.columns[[0, 1, 2, 3, 4, 5, 6, 7]], axis = 1)
t.drop(p.index[0:2])

