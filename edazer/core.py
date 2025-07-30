import pandas as pd
import polars as pl
from typing import List, Union, Dict
import warnings
from IPython import get_ipython

"""
- use in ipynb files as display() is involved
- few validation checks
"""

class Edazer: 
    """
    Exploratory data analyzer. Can be used to analyze multiple DataFrames separately,
    each as an instance of Edazer.

    Parameters
    ----------
    `df` : pd.DataFrame
        The DataFrame to analyze.

    `name` : str, optional
        Name of the DataFrame. If not provided, the analyzer will not display a name.

    `backend` : str, optional
    The backend to use for DataFrame operations. 
    Must be either `'pandas'` or `'polars'`. Defaults to `'pandas'`.

    Notes
    -------
        If the input DataFrame is not of the specified backend type, 
        it will be automatically converted.
    """

    __shell = get_ipython().__class__.__name__ 
    if __shell != "ZMQInteractiveShell":
        warnings.warn("Some methods may work only in a .ipynb file", UserWarning)

    @staticmethod
    def _validate_df(df):
        if not isinstance(df, (pd.DataFrame, pl.DataFrame)):
                raise TypeError(f"The Input dataframe must be a pandas Dataframe or polars dataframe\nBut received: {type(df)}")
     

    @staticmethod
    def pd_pl_conv(df: pd.DataFrame| pl.DataFrame):
        """
        Automatically converts between pandas Dataframe and polars DataFrame based on input Dataframe type
        - Converts to `polars.DataFrame` if input is a `pandas.DataFrame`.
        - Converts to `pandas.DataFrame` if input is a `polars.DataFrame`.

        Parameters
        ----------
        `df`: pd.DataFrame| pl.DataFrame
            The Dataframe to convert

        Returns
        -------
        `df` : `pandas.DataFrame` or `polars.DataFrame`
        """

        Edazer._validate_df(df)

        if isinstance(df, pd.DataFrame):
            return pl.from_pandas(df)                    # requires pyarrow to be installed
        return df.to_pandas()
    

    def __init__(self, df: pd.DataFrame| pl.DataFrame, backend= "pandas", name: str=None): 
        
        Edazer._validate_df(df)

        backend = backend.lower()
        if backend not in ("pandas", "polars"):
            raise ValueError("Backend must be either pandas or polars.")
        self._backend = backend

        if self._is_pandas_backend:
            self.df = Edazer.pd_pl_conv(df) if isinstance(df, pl.DataFrame) else df
        else:
            self.df = Edazer.pd_pl_conv(df) if isinstance(df, pd.DataFrame) else df
        
        self.__df_name = None
        if name is not None:
            self.__df_name = name

    @staticmethod
    def __version__(): # this method should be availble like edazer.__version__ not in Edazer, so maybe move it to __init__.py. use @property to it.
        """
        Returns the version of the Edazer class.
        """
        return "0.1.3"
    
    @property
    def _is_pandas_backend(self) -> bool:
        return self._backend == "pandas"
    
    @property
    def backend(self):
        return self._backend
    # to deine a func, giving users option to change backend for every ops. a setter fn

    def __repr__(self):
        if self.__df_name is not None:
            return f"Analyzer for the DataFrame: {self.__df_name}"
        else:
            return super().__repr__()

    def lookup(self, option: str= "head") -> pd.DataFrame:
        """
        Return a subset of the DataFrame.

        Parameters
        ----------
        `option` : str, optional 
        The option to choose. Defaults to "head".

        Options:
        ----------
        - 'head': Return the first few rows of the DataFrame.
        - 'tail': Return the last few rows of the DataFrame.
        - 'sample': Return a random sample of rows from the DataFrame.

        Returns
        -------
        pd.DataFrame
            The selected subset of the DataFrame.
        """
        
        option = option.lower()
        if (option == "head"):
            display(self.df.head())
        elif option == "tail":
            display(self.df.tail())
        elif option == "sample":
            display(self.df.sample())    
        else: 
            raise ValueError("Invalid option. Valid options are: head, tail, sample")    

    def summarize_df(self):
        """
        Summarizes the DataFrame by providing information about its 
        shape, null values, duplicated rows, unique values, and descriptive statistics.

        The following information is provided:
        - DataFrame info/ schema
        - Descriptive statistics (mean, std, min, 25%, 50%, 75%, 99%)
        - Number of null values
        - Number of duplicated rows
        - Number of unique values
        - DataFrame shape (number of rows and columns)
        """

        def pd_summarize_df(df = self.df):
            print("DataFrame Info:")
            print("-"*25) 
            df.info()
            print("\n")

            print("DataFrame Description:")
            print("-"*25) 
            display(df.describe(percentiles=[.25, .50, .75, .99]).T)
            print("\n")

            print("Number of Null Values:")
            print("-"*25) 
            display(df.isnull().sum()) 
            print("\n")

            print("Number of Duplicated Rows:")
            print("-"*25)
            display(int(df.duplicated().sum())) 
            print("\n")

            print("Number of Unique Values:")
            print("-"*25)
            display(df.nunique()) 
            print("\n")

            print("DataFrame Shape:")
            print("-"*25)
            print(f"No. of Rows:    {df.shape[0]}\nNo. of Columns: {df.shape[1]}")

        def pl_summarize_df(df = self.df):

            print("DataFrame Info:")
            print("-" * 25)
            display(df.schema)
            print("\n")

            print("DataFrame Description:")
            print("-"*25) 
            
            desc_df = df.describe(percentiles=(0.25, 0.5, 0.75, 0.99))
            stat_col = desc_df.columns[0] 
            new_column_names = [stat_col] + df.columns
            desc_df.columns = new_column_names
            display(desc_df)
            print("\n")

            print("Number of Null Values:")
            print("-" * 25)
            display(df.null_count())
            print("\n")

            print("Number of Duplicated Rows:")
            print("-" * 25)
            display(df.is_duplicated().sum())  
            print("\n")

            print("Number of Unique Values:")
            print("-" * 25)
            display(df.n_unique())
            print("\n")

            print("DataFrame Shape:")
            print("-" * 25)
            print(f"No. of Rows:    {df.height} \nNo. of Columns: {df.width}")

        if self._is_pandas_backend:
            pd_summarize_df()
        else:
            pl_summarize_df()

    def show_unique_values(self, column_names: List[str] = None, max_unique: int = 10):
        """
        Displays the unique values for specified columns.

        Parameters
        ----------
        column_names : List[str], optional
            List of column names to display unique values for.
            If None, defaults to object/category columns for pandas,
            and String/Categorical columns for polars.
        max_unique : int, optional
            The maximum number of unique values to display. Defaults to 10.

        Notes
        -----
        For numeric columns, pass the column names explicitly using `column_names`.
        If all selected columns exceed `max_unique` unique values, a message will
        suggest setting a higher threshold.
        """
        if not isinstance(max_unique, int):
            raise TypeError("'max_unique' must be an integer.")

        self._more_than_max_unique_cols = []

        if self._is_pandas_backend:
            if column_names is None:
                column_names = self.df.select_dtypes(include=["category", "object"]).columns

            for col in column_names:
                unique_vals = self.df[col].unique()
                if len(unique_vals) <= max_unique:
                    print(f"{col}: {list(unique_vals)}")
                else:
                    self._more_than_max_unique_cols.append(col)

        else:
            if column_names is None:
                column_names = [
                    col for col, dtype in zip(self.df.columns, self.df.dtypes)
                    if dtype in (pl.Utf8, pl.Categorical)
                ]

            for col in column_names:
                n_unique = self.df[col].n_unique()
                if n_unique <= max_unique:
                    unique_vals = list(self.df[col].unique())
                    print(f"{col}: {unique_vals}")
                else:
                    self._more_than_max_unique_cols.append(col)

        n_exceeding = len(self._more_than_max_unique_cols)
        if n_exceeding == len(column_names):
            print(f"All the mentioned columns have more than {max_unique} unique values.")
        elif n_exceeding > 0:
            print(f"\nColumns with more than {max_unique} unique values: {self._more_than_max_unique_cols}")
            print("Consider setting 'max_unique' to a higher value.")
        

    def cols_with_dtype(self, dtypes: List[str], exact: bool = False, return_dtype_map: bool = False
    ) -> Union[List[str], Dict[str, str]]:
        """
        Returns column names (or a mapping) of DataFrame columns matching specified data types.

        Parameters
        ----------
        dtypes : List[str]
            A list of data types (as strings) to match.
            Examples: ['int', 'float'], or ['int64', 'object']
        exact : bool, optional
            - If False (default), matches normalized types (e.g., 'float64' → 'float')
            - If True, requires exact string matches (e.g., 'float64' only matches 'float64')
        return_dtype_map : bool, optional
            If True, returns a dictionary {column_name: dtype}.
            If False (default), returns a list of matching column names.

        Returns
        -------
        List[str] or Dict[str, str]
            Either a list of column names or a mapping of column name to dtype.
        """

        if not isinstance(dtypes, list) or not all(isinstance(x, str) for x in dtypes):
            raise TypeError("`dtypes` must be a list of strings.")

        dtypes = [dt.lower().strip() for dt in dtypes]

        normalize_dtype = lambda dtype_str : ''.join(char for char in dtype_str.lower() if char.isalpha())

        result = {}

        if self._is_pandas_backend:
            for col in self.df.columns:
                col_dtype_str = str(self.df[col].dtype).lower()
                match_key = col_dtype_str if exact else normalize_dtype(col_dtype_str)
                if match_key in dtypes:
                    result[col] = col_dtype_str
        else:  # Polars
            for col, dtype in zip(self.df.columns, self.df.dtypes):
                col_dtype_str = str(dtype).lower()
                match_key = col_dtype_str if exact else normalize_dtype(col_dtype_str)
                if match_key in dtypes:
                    result[col] = col_dtype_str

        return result if return_dtype_map else list(result.keys())

