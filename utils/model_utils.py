import pandas as pd
import statsmodels.api as sm




def run_ols(df: pd.DataFrame, y: str, x: list):
X = df[x]
X = sm.add_constant(X)
model = sm.OLS(df[y], X, missing='drop').fit()
return model
