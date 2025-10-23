# Edazer

**Edazer** is a lightweight Python package for performing common exploratory data analysis (EDA) tasks.
It provides quick and intuitive methods to inspect, summarize, and understand datasets—supporting both pandas and polars backends.

*Kaggle Notebook quick tutorial on Edazer**: [https://www.kaggle.com/code/adarsh79x/edazer-for-quick-eda-pandas-polars-profiling]

Includes utilities for:
*Interactive DataFrame exploration* (via itables)

*Automated profiling reports* (via a wrapper around ydata-profiling)

*Unique key detection* (via get_primary_key)

🚀 Ideal for:

Jupyter notebooks

Fast, one-line data profiling

Early-stage dataset exploration

---

## Features

- **Quick DataFrame Summaries:** Instantly view info, describe, nulls, duplicates, and shape using `summary` method
- **Unique Value Inspection:** Easily display unique values for any or all columns.
- **Type-based Column Selection:** Find columns by dtype (e.g., int, float categorical).
- **Flexible Subsetting:** Use the `lookup` method to view head, tail, or random samples.
- **Custom DataFrame Naming:** Track multiple DataFrames with custom names for clarity.
- **Primary Key Detection:** Automatically identify single or multi-column combinations that can serve as unique identifiers.

---

## Installation

```bash
pip install edazer
```

---

## Quick Start with Titanic Dataset

```python
import seaborn as sns
from edazer import Edazer, interactive_df
from edazer.profiling import show_data_profile
from edazer import get_primary_key

# Enable interactive DataFrames (via itables)
interactive_df()

# Load dataset
titanic = sns.load_dataset('titanic')

# Initialize Edazer instance
titanic_dz = Edazer(titanic, backend="pandas", name="titanic")

# Complete DataFrame summary
titanic_dz.summarize_df()

# Data profiling report (via ydata_profiling)
show_data_profile(titanic_dz)

# Show unique values for specific columns
titanic_dz.show_unique_values(column_names=['class', 'embarked'], max_unique=5)

# Get float columns
print(titanic_dz.cols_with_dtype(['float'], exact=False))

# Combine methods: get object columns and show their unique values
titanic_dz.show_unique_values(column_names=titanic_dz.cols_with_dtype(dtypes=["object"]))

# To identify unique identifiers
get_primary_key(df, threshold=1.0, n_combos=2)

# View first few rows
print(titanic_dz.lookup("head"))

# Access raw DataFrame
print(titanic_dz.df.columns)


```

---

## 📘 API Reference

### `Edazer(df, backend="pandas", name=None)`

Create an analyzer instance.

- `df`: `pd.DataFrame` or `pl.DataFrame`  
- `backend`: `"pandas"` or `"polars"` (default: `"pandas"`)  
- `name`: Optional string label for the DataFrame

---

### `summarize_df()`

Print summary:

- Schema/info
- Descriptive stats
- Null/duplicate counts
- Unique values
- Shape

---

### `show_unique_values(column_names=None, max_unique=10)`

Show unique values for columns.

- `column_names`: Optional list of columns  
- `max_unique`: Max unique values to display per column

---

### `cols_with_dtype(dtypes, exact=False, return_dtype_map=False)`

Return columns matching specified dtypes.

- `dtypes`: List of type strings (e.g. `["int", "object"]`)  
- `exact`: Match full dtype string (e.g. `"int64"`)  
- `return_dtype_map`: If `True`, return `{col: dtype}`

---

### `lookup(option="head")`

Quickly inspect data.

- `option`: `"head"`, `"tail"`, or `"sample"`

---

### `🆕 get_primary_key(df, threshold=0.9, n_combos=1, valid_column_dtypes=None)`

Identify column(s) or column combinations that can serve as unique keys.

Parameters

- `df`  – The input DataFrame.

- `threshold` – Proportion of uniqueness required (default = 0.9).

- `n_combos`– Number of columns to combine when testing composite keys (default = 1).

- `valid_column_dtypes` – Data types to consider (default = ["int", "datetime64", "object"]).

Returns

List[str] or List[List[str]]: Candidate key columns or combinations that are likely unique identifiers.

#### Example usage

```python
from edazer import get_primary_key
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["A", "B", "C", "A"],
    "date": pd.date_range("2023-01-01", periods=4)
})

get_primary_key(df, threshold=1.0, n_combos=2)
# Output: [['id', 'name'], ['id', 'date'], ['name', 'date']]
```

## Example Output

```python
titanic_eda.show_unique_values(column_names=titanic_dz.cols_with_dtype(dtypes=["object"]))

# Output:
sex: ['male', 'female']
embarked: ['S', 'C', 'Q', nan]
who: ['man', 'woman', 'child']
embark_town: ['Southampton', 'Cherbourg', 'Queenstown', nan]
alive: ['no', 'yes']
```

---

## Contributing

Contributions are highly welcome! 

https://github.com/adarsh-79/edazer

---

## License

MIT License

---

## Author
[adarsh3690704](https://github.com/adarsh-79)
