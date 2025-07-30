from ydata_profiling import ProfileReport
import pandas as pd


def show_data_profile(df: pd.DataFrame):
    """
    Generates an interactive exploratory data analysis (EDA) report for the 
    given DataFrame using YData Profiling.
    """

    profile = ProfileReport(df, explorative=True)
    profile.to_notebook_iframe()


