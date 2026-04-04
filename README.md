# 🚀 edazer

**edazer** is a lightweight Python package designed to accelerate **exploratory data analysis (EDA)** workflows. It provides simple, intuitive, and consistent APIs to inspect, summarize, and understand datasets—supporting both **pandas** and **polars** backends.

Instead of rewriting repetitive EDA code for every project, **edazer** helps you get insights in just a few lines.

---

## 📓 Kaggle Tutorial

👉 Quick hands-on guide: ( uses previous version)
https://www.kaggle.com/code/adarsh79x/edazer-for-quick-eda-pandas-polars-profiling

---

## ✨ What’s New in `v0.2.0`

- Improved backend abstraction for **pandas & polars**
- Cleaner API for dtype-based column selection
- Enhanced unique value inspection
- Better handling of edge cases (non-hashable columns, dtype normalization)
- Internal performance and structure improvements

---

## 🎯 Use Cases

- ⚡ Quick dataset understanding
- 📊 Early-stage data exploration
- 📓 Jupyter notebook workflows
- 🔍 Identifying data quality issues
- 🧠 Feature understanding before modeling

---

## 🔧 Features

### 📌 DataFrame Summary

Get a complete overview in one call:

- Schema / info  
- Descriptive statistics  
- Null percentages  
- Duplicate count  
- Unique values  
- Shape  

```python
dz.summarize_df()
```

---

### 🔍 Smart Data Inspection

```python
dz.lookup("head")     # first rows
dz.lookup("tail")     # last rows
dz.lookup("sample")   # random sample
```

---

### 🧩 Unique Value Exploration

```python
dz.show_unique_values(
    column_names=["col1", "col2"],
    max_unique=10
)
```

- Automatically skips noisy columns  
- Suggests when to increase threshold  

---

### 🧠 Dtype-Based Column Selection

```python
dz.cols_with_dtype(["float", "int"])
```

Options:

- `exact=True` → strict dtype match (`float64`)  
- `return_dtype_map=True` → returns `{column: dtype}`  

---

### 🔑 Primary Key Detection

```python
from edazer import get_primary_key

get_primary_key(df, threshold=0.9, n_combos=2)
```

Find:

- Single-column unique identifiers  
- Multi-column composite keys  

---

### 📊 Data Profiling (Optional)

```python
from edazer.profiling import show_data_profile

show_data_profile(dz)
```

Powered by `ydata-profiling`.

---

### 🖱️ Interactive Tables

```python
from edazer import interactive_df

interactive_df()
```

Enables rich DataFrame viewing using `itables`.

---

## 📦 Installation

```bash
pip install edazer==0.2.0
```

---

## ⚡ Quick Start

```python
import seaborn as sns
from edazer import Edazer

# Load dataset
df = sns.load_dataset("titanic")

# Initialize
dz = Edazer(df, backend="pandas")

# Summary
dz.summarize_df()

# Unique values
dz.show_unique_values(column_names=["sex", "class"])

# Dtype filtering
print(dz.cols_with_dtype(["float"]))

# Inspect data
dz.lookup("head")
```

---

## 📘 API Reference

### `Edazer(df, backend="pandas")`

Create an analyzer instance.

- `df`: `pd.DataFrame` or `pl.DataFrame`  
- `backend`: `"pandas"` or `"polars"`  

---

### `summarize_df()`

Displays:

- Schema/info  
- Descriptive stats  
- Null/duplicate counts  
- Unique values  
- Shape  

---

### `show_unique_values(column_names, max_unique=10)`

- `column_names`: list of columns  
- `max_unique`: max values to display  

---

### `cols_with_dtype(dtypes=None, exact=False, return_dtype_map=False)`

- `dtypes`: list of dtype strings  
- `exact`: strict match  
- `return_dtype_map`: return dict instead of list  

---

### `lookup(option="head")`

- `"head"` → first rows  
- `"tail"` → last rows  
- `"sample"` → random rows  

---

### `get_primary_key(df, threshold=0.9, n_combos=1, valid_column_dtypes=None)`

Detect candidate keys.

Returns:

- `List[str]` or `List[List[str]]`

---

## 📊 Example Output

```python
dz.show_unique_values(
    column_names=dz.cols_with_dtype(["object"])
)
```

```
sex: ['male', 'female']
embarked: ['S', 'C', 'Q', nan]
class: ['Third', 'First', 'Second']
```

---

## 🤝 Contributing

Contributions are welcome!

GitHub: https://github.com/adarsh-79/edazer

---

## 📄 License

MIT License

---

## 👨‍💻 Author

[adarsh3690704](https://github.com/adarsh-79)
