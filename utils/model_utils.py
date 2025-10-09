import pandas as pd
import statsmodels.api as sm

def run_ols(df: pd.DataFrame, y_col: str, x_cols: list):
    X = sm.add_constant(df[x_cols])
    y = df[y_col]
    model = sm.OLS(y, X).fit()
    return model

def run_logit(df: pd.DataFrame, y_col: str, x_cols: list):
    X = sm.add_constant(df[x_cols])
    y = df[y_col]
    model = sm.Logit(y, X).fit(disp=0)
    return model
