import pandas as pd


class Data_Output:
    df: pd.DataFrame

    SP2R=["stk on start","prj on start", "risk on destination"]
    PR2S=["prj on start", "risk on start", "stk on destination"]
    P2SR=["prj on start", "stk on destination","risk on destination"]

    def __init__(self):
        ...

    def df_input(self, df):
        if not df: raise Exception("An empty dataframe been passed.")
        self.df=df
        return

    def testing(self, args:pd.Series):
        for _, val in args.items():
            if not val: return 0
        return 1


    def validate_frequency_set(self):
        self.df["SP2R"]=self.df[self.SP2R].apply(self.testing, axis=1)
        self.df["PR2S"]=self.df[self.PR2S].apply(self.testing, axis=1)
        self.df["P2SR"]=self.df[self.P2SR].apply(self.testing, axis=1)
        return self.df

    def data_ratio_check(self):
        sp2r=(self.df["stk on start"].sum()+self.df["prj on start"].sum())/self.df["risk on start"].sum()
        pr2s=(self.df["risk on start"].sum()+self.df["prj on start"].sum())/self.df["stk on start"].sum()
        p2rs=self.df["prj on start"].sum()/(self.df["risk on start"].sum()+self.df["stk on start"].sum())
        return pd.DataFrame([sp2r, pr2s, p2rs], index=["sp2r", "pr2s", "p2rs"], columns=["convertion rate"])
