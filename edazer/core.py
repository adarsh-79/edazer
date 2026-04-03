import pandas as pd
import polars as pl

from typing import Callable
from IPython import get_ipython
import warnings


def _smart_display(obj):
    """Displays an object using IPython's display if available, else prints."""
    try:
        from IPython.display import display
        display(obj)
    except ImportError:
        print(obj)

class _PandasEngine:
    def __init__(self, df: pd.DataFrame):
         self.df = df
        
    def summarize_df(self):
            print("DataFrame Info:")
            print("-"*25) 
            _smart_display(self.df.info())
            print("\n")

            print("DataFrame Description:")
            print("-"*25) 
            _smart_display(self.df.describe(percentiles=[.25, .50, .75, .99]).T)
            print("\n")

            print("Percentage of Null Values:")
            print("-"*25) 
            _smart_display((self.df.isnull().sum() / len(self.df)) * 100)
            print("\n")

            print("Number of Duplicated Rows:")
            print("-"*25)
            _smart_display(int(self.df.duplicated().sum())) 
            print("\n")

            print("Number of Unique Values:")
            print("-"*25)
            _smart_display(self.df.nunique()) 
            print("\n")

            print("DataFrame Shape:")
            print("-"*25)
            print(f"No. of Rows:    {self.df.shape[0]}\nNo. of Columns: {self.df.shape[1]}")

    def show_unique_values(self, column_names: list[str], max_unique: int):
        more_than_max_unique_cols = []

        for col in column_names:
            unique_vals = self.df[col].unique()
            if len(unique_vals) <= max_unique:
                    print(f"{col}: {list(unique_vals)}")
            else:
                more_than_max_unique_cols.append(col)

        return more_than_max_unique_cols
    
    def cols_with_dtype(self, normalize_dtype: Callable[[str], str], dtypes: list[str], exact: bool = False) -> list[str] | dict[str, str]:
        result = {}

        for col in self.df.columns:
            col_dtype_str = str(self.df[col].dtype)
            match_key = col_dtype_str if exact else normalize_dtype(col_dtype_str)
            if match_key in dtypes:
                result[col] = col_dtype_str
        return result

class _PolarsEngine:
    
    def __init__(self, df: pl.DataFrame):
         self.df = df
    
    def summarize_df(self):
        
        print("DataFrame Info:")
        print("-" * 25)
        _smart_display(self.df.schema)
        print("\n")

        print("DataFrame Description:")
        print("-"*25) 
           
        desc_df = self.df.describe(percentiles=(0.25, 0.5, 0.75, 0.99))
        stat_col = desc_df.columns[0] 
        new_column_names = [stat_col] + self.df.columns
        desc_df.columns = new_column_names
        _smart_display(desc_df)
        print("\n")

        print("Percentage of Null Values:")
        print("-" * 25)
        null_counts = self.df.null_count()
        null_percent = (null_counts / self.df.height) * 100
        _smart_display(null_percent)
        print("\n")

        print("Number of Duplicated Rows:")
        print("-" * 25)
        _smart_display(self.df.is_duplicated().sum())  
        print("\n")

        print("Number of Unique Values:")
        print("-" * 25)
        _smart_display(self.df.n_unique())
        print("\n")

        print("DataFrame Shape:")
        print("-" * 25)
        print(f"No. of Rows:    {self.df.height} \nNo. of Columns: {self.df.width}")
    
    def show_unique_values(self, column_names: list[str], max_unique: int = 10):
        more_than_max_unique_cols = []

        for col in column_names:
            try:
                n_unique = self.df[col].n_unique()
                if n_unique <= max_unique:
                    unique_vals = list(self.df[col].unique())
                    print(f"{col}: {unique_vals}")
                else:
                    more_than_max_unique_cols.append(col)
            except Exception:
                # Skip non-hashable or problematic columns
                continue

        return more_than_max_unique_cols

    def cols_with_dtype(self, normalize_dtype: Callable[[str], str], dtypes: list[str], exact: bool = False) -> list[str] | dict[str, str]:
        result = {}

        for col, dtype in zip(self.df.columns, self.df.dtypes):
            if not exact:
                dtype_str = str(dtype).lower()
            else:
                dtype_str = str(dtype)
    
            if dtype == pl.Categorical:
                dtype_str = "categorical"
    
            if dtype_str in dtypes:
                result[col] = str(dtype)

        return result

def _check_ipynb(func):
    def wrapper(*args, **kwargs): 
        ip = get_ipython()
        if ip is None or ip.__class__.__name__ != "ZMQInteractiveShell":
            warnings.warn("Certain elements looks better  visually in Jupyter (.ipynb) environments.", UserWarning)
        return func(*args, **kwargs)
    return wrapper


class Edazer:
    """
        Initialize the Edazer analyzer.

        Parameters
        ----------
        df : pandas.DataFrame or polars.DataFrame
            The DataFrame to analyze.
        backend : str, optional
            Backend to use ("pandas" or "polars"). Default is "pandas".

        Raises
        ------
        TypeError
            If DataFrame type does not match backend.
    """

    def __init__(self, df: pd.DataFrame | pl.DataFrame, backend: str = "pandas"):
        backend = backend.lower()
        if backend not in ("pandas", "polars"):
            raise ValueError("Backend must be either pandas or polars.")
        self._backend = backend
        
        self._is_pandas_backend = True if self._backend == "pandas" else False

        if self._is_pandas_backend:
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"df must be a pandas DataFrame for pandas backend but got {type(df)}")
        else:
            if not isinstance(df, pl.DataFrame):
                raise TypeError(f"df must be a polars DataFrame for polars backend but got {type(df)}")
        self.df = df

        self.engine = _PandasEngine(self.df) if self._is_pandas_backend else _PolarsEngine(self.df)
    
    @property
    def backend(self):
        return self._backend
    
    @_check_ipynb
    def lookup(self, option: str= "head"):
        """
        Display a subset of the DataFrame.

        Parameters
        ----------
        option : str, optional
            Type of subset to display:
            - "head": first few rows
            - "tail": last few rows
            - "sample": random sample
        """

        option = option.lower()
        if (option == "head"):
            _smart_display(self.df.head())
        elif option == "tail":
            _smart_display(self.df.tail())
        elif option == "sample":
            _smart_display(self.df.sample(n=5))    
        else: 
            raise ValueError("Invalid option. Valid options are: head, tail, sample")

    @_check_ipynb
    def summarize_df(self):
        """
        Display a comprehensive summary of the DataFrame.
        """
        return self.engine.summarize_df()
    
    def __call__(self):
        return self.summarize_df()

    def show_unique_values(self, column_names: list[str], max_unique: int = 10):
        """
        Displays the unique values for specified columns.

        Parameters
        ----------
        column_names : List[str]
            List of column names to display unique values for.
        max_unique : int, optional
            The maximum number of unique values of a column to display. Defaults to 10.
        """

        if not isinstance(max_unique, int):
            raise TypeError("'max_unique' must be an integer.")

        more_than_max_unique_cols = self.engine.show_unique_values(column_names=column_names, max_unique=max_unique)
        
        n_exceeding = len(more_than_max_unique_cols)  
        
        if len(column_names)==0:
            print("'column_names' is a empty list!")
            return  
        
        if n_exceeding == len(column_names):
            print(f"All the mentioned columns have more than {max_unique} unique values.")
        elif n_exceeding > 0:
            print(f"\nColumns with more than {max_unique} unique values: {more_than_max_unique_cols}")
            print("Consider setting 'max_unique' to a higher value.")
        
    def cols_with_dtype(self, dtypes: list[str] | None = None, exact: bool = False, return_dtype_map: bool = False
    ) -> list[str] | dict[str, str]:
        """
        Retrieve columns matching specified data types.

        Parameters
        ----------
        dtypes : list of str, optional
            Data types to match. Defaults to categorical/string types.
        exact : bool, optional
            If True, requires exact dtype match.
        return_dtype_map : bool, optional
            If True, returns a mapping {column: dtype}.
            Otherwise, returns a list of column names.

        Returns
        -------
        list or dict
            Matching column names or mapping of column names to dtypes.
        """

        if dtypes is None:
            if self._is_pandas_backend:
                dtypes = ["object", "category"]
            else:
                dtypes = ["utf8", "categorical"]
        
        if (not isinstance(dtypes, list)) or (not all(isinstance(x, str) for x in dtypes)):
            raise TypeError("`dtypes` must be a list of strings.")
        
        dtypes = [dt.lower().strip() for dt in dtypes]
        
        normalize_dtype = lambda dtype_str : ''.join(char for char in dtype_str.lower() if char.isalpha())
        result = self.engine.cols_with_dtype(normalize_dtype=normalize_dtype, dtypes=dtypes, exact=exact)
        
        return result if return_dtype_map else list(result.keys())
    
__all__ = [Edazer]

if __name__ == "__main__":
    import seaborn as sns
    df = sns.load_dataset("tips")
    print(df.dtypes)

    df_zer = Edazer(df)
    print(df_zer.cols_with_dtype(["float64"], exact=True))