# Module 3: Data Manipulation with pandas

> See `COURSE_OUTLINE.md` at the repo root for full lesson objectives, durations, and
> deliverables.

Every worked example in this module uses the same three-table "online store" dataset
you'll keep using through Modules 4-6: `customers`, `products`, and `orders`. See
`data/README.md` for the full schema and the specific data-quality issues baked into it
on purpose (messy `region` text, missing values, duplicate `order_id` rows, orphan
`customer_id` rows). You'll fix every one of those issues somewhere in this module —
that's not a coincidence, it's the point. Always load the data with the loader
functions, never a hardcoded path:

```python
from data_science_course.datasets import load_customers, load_products, load_orders

customers = load_customers()
products = load_products()
orders = load_orders()
```

---

## Lesson 3.1 — Series and DataFrame Basics

### Why pandas?

In Module 2 you stored tabular-ish data in lists of dicts — one dict per row, one key
per column. That works, but it's slow and clunky once you have thousands of rows: no
built-in way to compute a column average, filter rows, or join two tables together.
**pandas** is a library built specifically for tabular data — rows and columns, like a
spreadsheet — and it makes those operations fast and short to write.

If you've ever used a spreadsheet (Excel, Google Sheets), the mental model transfers
almost directly:

| Spreadsheet term | pandas term |
|---|---|
| A whole sheet/table | `DataFrame` |
| One column of a sheet | `Series` |
| The row numbers down the left edge | the **index** |
| The header row | the column names (`.columns`) |
| One cell | one value, found by (row, column) |

If you've never used a spreadsheet either, that's fine — think of a `DataFrame` as "a
list of dicts that all share the same keys, glued together into one rectangular object
with fast operations."

### `Series`: one column

A `Series` is a one-dimensional, labeled array — a single column of data, plus an index
that labels each value.

```python
import pandas as pd

ages = pd.Series([34, 28, 45, 31], name="age")
print(ages)
```
```
0    34
1    28
2    45
3    31
Name: age, dtype: int64
```

The left column (`0, 1, 2, 3`) is the **index** — a label for each row, not part of the
data itself. By default it's just 0, 1, 2, ... but it doesn't have to be:

```python
ages = pd.Series([34, 28, 45, 31], index=["c1", "c2", "c3", "c4"], name="age")
print(ages["c3"])
```
```
45
```

`dtype: int64` tells you every value in this Series is a 64-bit integer. A Series (and
every column of a DataFrame) holds one dtype at a time — mixing an int and a string in
the same column silently upgrades the whole column to `object` (pandas' catch-all "it
could be anything, including Python objects" dtype), which is slower and loses type
safety. Keeping columns single-typed is worth watching for as you clean data later in
this module.

### `DataFrame`: the whole table

A `DataFrame` is a collection of Series that all share the same index — in other words,
a 2D table. You can build one directly from a dict of lists (each key becomes a column):

```python
sample = pd.DataFrame({
    "customer_id": ["C00001", "C00002", "C00003"],
    "region": ["North", "South", "West"],
    "age": [34, 28, 45],
})
print(sample)
```
```
  customer_id region  age
0      C00001  North   34
1      C00002  South   28
2      C00003   West   45
```

Or from a list of dicts (each dict becomes a row) — this is the shape you're used to
from Module 2:

```python
rows = [
    {"customer_id": "C00001", "region": "North", "age": 34},
    {"customer_id": "C00002", "region": "South", "age": 28},
]
pd.DataFrame(rows)
```

Picking out one column gives you back a `Series`:

```python
type(sample["age"])
```
```
<class 'pandas.core.series.Series'>
```

### Inspecting a real DataFrame

From here on, we use the real course dataset instead of toy examples. Load the
customers table:

```python
from data_science_course.datasets import load_customers

customers = load_customers()
customers.head()
```
```
  customer_id signup_date region  ...  membership_tier acquisition_channel churned
0      C00001  2022-09-08  SOUTH  ...           Silver            referral       1
1      C00002  2024-07-22   west  ...           Bronze               email       0
2      C00003  2024-07-15  north  ...             Gold              social       1
3      C00004  2023-06-16  south  ...           Silver         paid_search       0
4      C00005  2024-08-17   WEST  ...           Silver             organic       0

[5 rows x 7 columns]
```

`.head()` shows the first 5 rows by default (pass a number, e.g. `.head(10)`, for more).
Already you can spot something worth remembering for Lesson 3.4/3.5: the `region`
column is spelled inconsistently (`SOUTH`, `west`, `north`, `WEST`) — that's one of the
deliberate data-quality issues described in `data/README.md`, and you'll clean it up
soon. Don't fix it yet — for now, just get comfortable inspecting the data as-is.

`.shape` gives you (rows, columns) as a tuple, and `.columns` lists the column names:

```python
print(customers.shape)
print(list(customers.columns))
```
```
(800, 7)
['customer_id', 'signup_date', 'region', 'age', 'membership_tier', 'acquisition_channel', 'churned']
```

`.info()` is usually the first thing to run on any new DataFrame — it shows dtypes and,
critically, non-null counts per column (a quick way to spot missing data):

```python
customers.info()
```
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 800 entries, 0 to 799
Data columns (total 7 columns):
 #   Column               Non-Null Count  Dtype  
---  ------               --------------  -----  
 0   customer_id          800 non-null    object 
 1   signup_date          800 non-null    object 
 2   region               776 non-null    object 
 3   age                  752 non-null    float64
 4   membership_tier      800 non-null    object 
 5   acquisition_channel  800 non-null    object 
 6   churned              800 non-null    int64  
dtypes: float64(1), int64(1), object(5)
memory usage: 43.9+ KB
```

800 rows total, but `region` only has 776 non-null values and `age` only has 752 — so
24 rows are missing a region and 48 are missing an age. We'll deal with that properly in
Lesson 3.5. Note also that `signup_date` shows up as `object` (plain text), not a date —
`pd.read_csv` doesn't guess dates automatically; Lesson 3.2 shows how to parse it.

`.describe()` gives summary statistics, but only for numeric columns by default:

```python
customers.describe()
```
```
              age     churned
count  752.000000  800.000000
mean    37.470745    0.562500
std     11.580285    0.496389
min     18.000000    0.000000
25%     29.000000    0.000000
50%     38.000000    1.000000
75%     46.000000    1.000000
max     76.000000    1.000000
```

Note `count` for `age` is 752, matching `.info()` — `.describe()` automatically skips
missing values rather than erroring or treating them as 0. `churned` is technically a
0/1 integer column (our future classification target — see Lesson 4.x), so its "mean"
here is really just the fraction of customers who churned (~56%).

### The index, revisited

Every DataFrame has an index, whether you set one or not. `load_customers()` gives you
the default `RangeIndex` (0, 1, 2, ...), but you can point at a more meaningful column
instead — useful when a column is a natural unique key:

```python
by_id = customers.set_index("customer_id")
by_id.loc["C00003"]
```
```
signup_date             2024-07-15
region                        north
age                             NaN
membership_tier                Gold
acquisition_channel           social
churned                            1
Name: C00003, dtype: object
```

`set_index()` returns a *new* DataFrame by default (the original `customers` is
untouched) — this "returns a new object instead of modifying in place" pattern shows up
constantly in pandas, and it's worth internalizing now: nearly every method you call
(`.rename()`, `.drop()`, `.sort_values()`, `.fillna()`, ...) returns a new DataFrame
unless you pass `inplace=True` or reassign the result yourself.

**Try it yourself and see the full worked examples in the notebook:**
`modules/03-pandas/notebooks/3.1-series-and-dataframe-basics.ipynb`

---

## Lesson 3.2 — Reading and Writing Data

### `load_customers()` is a thin wrapper around `pd.read_csv`

The loader functions you've been using all module are just convenience wrappers. Under
the hood, `load_customers()` does essentially:

```python
import pandas as pd
customers = pd.read_csv("data/raw/customers.csv")
```

pandas can read (and write) a lot of formats, each with a matching `pd.read_*` /
`.to_*` pair:

| Format | Read | Write |
|---|---|---|
| CSV | `pd.read_csv(path)` | `df.to_csv(path)` |
| Excel | `pd.read_excel(path)` | `df.to_excel(path)` |
| JSON | `pd.read_json(path)` | `df.to_json(path)` |

In this course you'll always use `load_customers()` / `load_products()` /
`load_orders()` instead of calling `pd.read_csv` directly — they guarantee you and every
other learner are working from the exact same file, regenerated deterministically if
it's ever missing. But you still need to know how `pd.read_*` and `df.to_*` work,
because in Module 6 (and real projects) you'll be loading data no one has wrapped a
loader function around.

### Common loading issues

`pd.read_csv` guesses a lot for you (delimiter detection, dtypes) but three things trip
up beginners constantly:

**1. Delimiter.** Not every "CSV" actually uses commas — some exports use semicolons or
tabs. If a file loads as a single garbled column, check the delimiter:

```python
pd.read_csv("some_file.csv", sep=";")   # semicolon-delimited
pd.read_csv("some_file.tsv", sep="\t")  # tab-delimited
```

**2. Header row not on line 1.** Some exported files have a title or metadata line
before the real header. `header=` tells pandas which row (0-indexed) has the column
names:

```python
pd.read_csv("exported_report.csv", header=2)  # real header is the 3rd line
```

**3. Encoding.** Files with non-ASCII characters (accented names, currency symbols)
sometimes aren't UTF-8. A `UnicodeDecodeError` when reading is the tell — try:

```python
pd.read_csv("legacy_export.csv", encoding="latin1")
```

**4. Dates load as text.** As you saw in Lesson 3.1, `signup_date` loads as `object`
(plain strings), not a real date type, unless you tell pandas which columns to parse:

```python
customers = pd.read_csv("data/raw/customers.csv", parse_dates=["signup_date"])
customers["signup_date"].dtype
```
```
dtype('<M8[ns]')
```

That `datetime64[ns]` dtype is what unlocks date arithmetic later (e.g. "how many days
since signup?"), instead of treating dates as un-comparable strings.

### Writing data back out

`.to_csv()` writes a DataFrame to disk. By default it also writes the index as a column
— usually not what you want for a plain `RangeIndex`, so pass `index=False`:

```python
cleaned = customers.copy()
cleaned["region"] = cleaned["region"].str.strip().str.lower().str.title()
cleaned.to_csv("modules/03-pandas/notebooks/scratch/customers_cleaned.csv", index=False)
```

Forgetting `index=False` is one of the most common beginner mistakes — it adds an extra
`Unnamed: 0` column when you read the file back in later.

### Excel files

`openpyxl` (already installed in this project) is what pandas uses under the hood to
read and write `.xlsx` files. The API mirrors CSV:

```python
products = load_products()
products.head(20).to_excel("modules/03-pandas/notebooks/scratch/top_products.xlsx", index=False)

reloaded = pd.read_excel("modules/03-pandas/notebooks/scratch/top_products.xlsx")
reloaded.head()
```

A multi-sheet workbook needs `sheet_name=`:

```python
pd.read_excel("workbook.xlsx", sheet_name="Q1")       # one sheet by name
pd.read_excel("workbook.xlsx", sheet_name=None)        # dict of {sheet_name: DataFrame}, all sheets
```

### JSON

Nested JSON (a list of records) reads similarly:

```python
products.head(5).to_json("modules/03-pandas/notebooks/scratch/products_sample.json", orient="records")
pd.read_json("modules/03-pandas/notebooks/scratch/products_sample.json")
```

`orient="records"` writes `[{"col": val, ...}, {"col": val, ...}, ...]` — the most
common and most portable shape for tabular JSON. Other `orient` values exist for less
common layouts; you won't need them in this course.

A note on the `scratch/` folder used above: notebooks in this module write files there
purely for exercise practice (reading back what you just wrote). It's exercise output
only, not course material — nothing else in the course reads from it.

**Full worked examples (including writing then re-reading a CSV and an Excel file) are
in the notebook:** `modules/03-pandas/notebooks/3.2-reading-and-writing-data.ipynb`

---

## Lesson 3.3 — Selecting and Filtering Rows/Columns

### Selecting columns with `[]`

A single column name in `[]` gives you a `Series`; a *list* of column names gives you
back a `DataFrame` (even a list of one):

```python
orders = load_orders()

orders["order_total"]           # Series
orders[["order_total"]]         # DataFrame, one column
orders[["order_id", "order_total", "status"]]   # DataFrame, three columns
```

### `.loc` and `.iloc`

`[]` alone gets ambiguous once you need rows too. pandas gives you two dedicated
selectors:

- **`.loc[row_labels, column_labels]`** — selects by *label* (the index value, and
  column names)
- **`.iloc[row_positions, column_positions]`** — selects by *integer position*, like
  Python list indexing, regardless of what the labels are

```python
by_id = orders.set_index("order_id")

by_id.loc["O000001"]                        # one row, by its label
by_id.loc["O000001", "order_total"]         # one cell
by_id.loc[["O000001", "O000002"], ["order_total", "status"]]  # sub-table by labels

orders.iloc[0]              # first row, by position
orders.iloc[0:3]            # first three rows, by position
orders.iloc[0:3, 0:2]       # first three rows, first two columns
```

A common beginner trip-up: `.loc` slicing with `:` is **inclusive of the end label**
(`.loc[0:3]` includes row label `3`), while `.iloc` slicing follows normal Python
rules and is **exclusive of the end** (`.iloc[0:3]` gives positions 0, 1, 2 — three
rows, not four). This is a real and common source of off-by-one bugs — when in doubt,
check `len()` of what you got back.

### Filtering with boolean masks

This is the pandas equivalent of a spreadsheet filter, and it's the idiom you'll use
constantly. A comparison against a Series produces a Series of `True`/`False` — a
**boolean mask** — and indexing a DataFrame with that mask keeps only the `True` rows:

```python
mask = orders["status"] == "cancelled"
mask.head()
```
```
0    False
1    False
2    False
3    False
4    False
Name: status, dtype: bool
```

```python
cancelled = orders[mask]
cancelled.shape
```
```
(191, 11)
```

Writing it in the explicit two-step form above (build the mask, then index with it)
makes it obvious what's happening, and it's exactly equivalent to the more common
one-liner `orders[orders["status"] == "cancelled"]`. Once the mask idiom feels natural,
reach for the one-liner — but build the explicit version first while you're learning.

`.loc` also accepts a boolean mask, and it's the right tool when you want to filter
rows **and** pick specific columns in one step:

```python
orders.loc[orders["status"] == "cancelled", ["order_id", "customer_id", "order_total"]]
```

### Combining conditions

Python's `and`/`or`/`not` don't work element-by-element on a Series (a Series of many
booleans can't collapse to one), so pandas uses the bitwise operators `&`, `|`, `~`
instead — and **each condition must be wrapped in parentheses**, because `&`/`|` bind
more tightly than comparison operators in Python:

```python
big_discount_returns = orders[
    (orders["status"] == "returned") & (orders["discount_pct"] > 0.15)
]
big_discount_returns.shape
```
```
(48, 11)
```

```python
credit_or_paypal = orders[
    (orders["payment_method"] == "credit_card") | (orders["payment_method"] == "paypal")
]
```

For "is this value one of several options," `.isin()` is cleaner than chaining `|`:

```python
credit_or_paypal = orders[orders["payment_method"].isin(["credit_card", "paypal"])]

not_credit = orders[~orders["payment_method"].isin(["credit_card"])]  # ~ negates
```

### Finding the duplicate orders

Recall from `data/README.md` that `orders.csv` has 5 exact duplicate `order_id` rows on
purpose. `.duplicated()` returns a boolean mask, `True` for rows that are duplicates of
an earlier row — this is exactly the boolean-mask-filtering pattern above, applied to
find bad data:

```python
dupe_mask = orders.duplicated(subset=["order_id"], keep="first")
orders[dupe_mask]
```
```
     order_id customer_id product_id  order_date  quantity     status
1184  O001727      C00272      P0021  2024-06-25         2  completed
1538  O001457      C00272      P0041  2023-07-11         2  cancelled
2862  O004417      C00701      P0003  2023-06-30         1  completed
4430  O002848      C00514      P0001  2023-11-04         1  completed
5414  O001907      C00021      P0057  2024-08-11         1  completed
```

Five rows come back — matching the count documented in `data/README.md`. `keep="first"`
(the default) marks every occurrence *after* the first as a duplicate, so
`orders[dupe_mask]` shows you exactly the extra rows you'd remove; we'll actually remove
them with `.drop_duplicates()` in Lesson 3.4.

### Sorting and sampling

```python
orders.sort_values("order_total", ascending=False).head(5)   # biggest orders first
orders.sort_values(["status", "order_total"], ascending=[True, False])  # multi-column

orders.sample(5, random_state=42)   # 5 random rows, reproducible with a fixed seed
```

Always pass `random_state=` when sampling in this course (we use `42` throughout) so
your output matches what's shown in notes/slides and reruns are reproducible.

**Full worked examples are in the notebook:**
`modules/03-pandas/notebooks/3.3-selecting-and-filtering.ipynb`

---

## Lesson 3.4 — Renaming, Adding, and Dropping Columns

### Renaming columns

`.rename(columns={...})` renames specific columns and, like most pandas methods,
returns a *new* DataFrame by default:

```python
customers = load_customers()

renamed = customers.rename(columns={"acquisition_channel": "channel"})
renamed.columns
```
```
Index(['customer_id', 'signup_date', 'region', 'age', 'membership_tier',
       'channel', 'churned'],
      dtype='object')
```

To rename *every* column at once, reassign `.columns` directly with a same-length list:

```python
renamed.columns = [c.upper() for c in renamed.columns]
```

Either way, prefer reassigning the result (`customers = customers.rename(...)`) or
using `inplace=True` deliberately, rather than leaving a renamed copy unused — a
frequent beginner bug is calling `.rename()` without doing either and then being
confused that the original column names didn't change.

### Cleaning up `region` — a real vectorized-string example

This is the moment to fix the messy `region` column documented in `data/README.md`.
String methods on a Series live under the `.str` accessor and apply to every value at
once — no loop needed:

```python
customers["region"].value_counts(dropna=False)
```
```
region
East      101
east       86
South      78
south      75
west       72
WEST       70
West       58
north      53
SOUTH      51
 North     51
NORTH      41
North      40
NaN       24
Name: count, dtype: int64
```

Twelve different spellings of four real regions, plus missing values. Chain three
`.str` methods to normalize casing and whitespace in one line:

```python
customers["region"] = (
    customers["region"]
    .str.strip()
    .str.lower()
    .str.title()
)
customers["region"].value_counts(dropna=False)
```
```
region
South    204
West     200
East     187
North    185
NaN       24
Name: count, dtype: int64
```

Down to exactly the four canonical regions, plus the genuinely-missing rows (which
`.str.title()` leaves as `NaN` — string methods pass missing values through unchanged
rather than erroring). This is a **vectorized operation**: pandas applies `.str.strip()`
to all 800 values internally, in compiled code, without you writing a Python-level
`for` loop. Vectorized operations are almost always faster than looping over rows
yourself, and you should reach for them first.

### Adding new columns

The simplest way to add a column is a vectorized arithmetic expression, assigned to a
new column name:

```python
orders = load_orders()

orders["revenue_per_unit"] = orders["order_total"] / orders["quantity"]
orders[["order_id", "quantity", "order_total", "revenue_per_unit"]].head(3)
```
```
   order_id  quantity  order_total  revenue_per_unit
0  O000080         1        72.48             72.48
1  O002751         1        69.18             69.18
2  O003297         1       201.03            201.03
```

This works because pandas aligns Series by index and applies the operation
element-by-element — again, vectorized, no loop.

For logic that isn't simple arithmetic — e.g. "bucket this order into a size category"
— reach for `.apply()`, which runs a Python function once per value (or once per row,
with `axis=1`):

```python
def size_bucket(total: float) -> str:
    if total < 50:
        return "small"
    elif total < 150:
        return "medium"
    return "large"

orders["order_size"] = orders["order_total"].apply(size_bucket)
orders["order_size"].value_counts()
```
```
order_size
large     2631
small     1742
medium    1636
Name: count, dtype: int64
```

`.apply()` is more flexible than a vectorized expression but slower, because it falls
back to calling your Python function once per row instead of running in compiled code.
For anything expressible as arithmetic or built-in `.str`/comparison operations, prefer
the vectorized form; save `.apply()` for genuinely custom per-row logic like this.

`np.where` (or a chain of `.loc` assignments) is a faster, still-vectorized alternative
for simple if/else column logic — worth knowing once `.apply()` starts feeling slow on
larger data:

```python
import numpy as np

orders["is_discounted"] = np.where(orders["discount_pct"] > 0, "yes", "no")
```

### Dropping columns and rows

`.drop()` removes columns (`axis=1` or `columns=`) or rows (`axis=0`, the default, by
index label):

```python
trimmed = orders.drop(columns=["revenue_per_unit", "order_size"])
orders_no_row0 = orders.drop(index=0)
```

Now put `.drop_duplicates()` to use on the 5 duplicate `order_id` rows you *found* with
`.duplicated()` in Lesson 3.3:

```python
print(orders.shape)
orders = orders.drop_duplicates(subset=["order_id"], keep="first")
print(orders.shape)
```
```
(6009, 13)
(6004, 13)
```

Five rows gone, matching exactly what `data/README.md` documents. `keep="first"` keeps
the first occurrence of each `order_id` and drops the rest — the usual choice, since the
duplicates here are exact copies and it doesn't matter which copy survives.

**Full worked examples are in the notebook:**
`modules/03-pandas/notebooks/3.4-rename-add-drop-columns.ipynb`

---

## Lesson 3.5 — Handling Missing Data

### Detecting missing values

pandas represents "no value" as `NaN` (Not a Number, for numeric columns) or `None`
(for object columns) — both show up as missing under `.isna()` (an alias, `.isnull()`,
does the same thing; use whichever reads better to you). `.isna()` on a DataFrame
returns a same-shaped DataFrame of booleans; sum it per column to count missing values
(`.sum()` on a boolean Series/DataFrame treats `True` as 1):

```python
customers = load_customers()
customers.isna().sum()
```
```
customer_id             0
signup_date             0
region                 24
age                    48
membership_tier         0
acquisition_channel     0
churned                 0
dtype: int64
```

This matches `data/README.md`: `region` is ~3% missing (24 of 800), `age` is ~6% missing
(48 of 800). To count rows with *at least one* missing value anywhere:

```python
customers.isna().any(axis=1).sum()
```
```
72
```

72 rows have a gap somewhere — more than 24 + 48 would suggest, meaning some rows are
missing *both* `region` and `age` at once, which is worth checking directly:

```python
customers[customers["region"].isna() & customers["age"].isna()].shape
```

### Deciding: drop or fill?

There's no single right answer — it depends on how much data you'd lose and what the
missingness means. Two tools, two philosophies:

**`.dropna()` — remove rows (or columns) with missing values.** Simple, but throws away
whatever else was in that row, even columns you cared about.

```python
customers.dropna().shape          # drop any row missing ANY column
```
```
(728, 7)
```

Dropping every row with *any* missing value drops 72 of 800 rows (9%) — probably too
aggressive here, since most of those rows have perfectly good data in every column
except one. Narrowing to a specific column with `subset=` is usually better:

```python
customers.dropna(subset=["region"]).shape   # only drop rows missing `region` specifically
```
```
(776, 7)
```

**`.fillna()` — replace missing values with something else.** Keeps every row, but you
have to choose a sensible fill value per column; picking a bad one quietly biases your
data.

```python
median_age = customers["age"].median()
customers["age"] = customers["age"].fillna(median_age)
customers["age"].isna().sum()
```
```
0
```

Filling numeric columns with the **median** (rather than the mean) is a common default
because the median is less sensitive to outliers. For a categorical column like
`region`, a common approach is a placeholder category rather than a statistic:

```python
customers["region"] = customers["region"].fillna("Unknown")
customers["region"].value_counts(dropna=False)
```
```
region
East       101
east        86
South       78
south       75
west        72
WEST        70
West        58
north       53
SOUTH       51
 North      51
NORTH       41
North      40
Unknown     24
Name: count, dtype: int64
```

(Notice `region` is still messy here — this lesson's examples work on the raw
column deliberately to keep missing-data handling isolated from the string-cleaning
from Lesson 3.4; in the notebook and in practice you'd normalize casing *and* fill
missing values together.)

### A column where "missing" doesn't mean "zero"

`orders["discount_pct"]` is the case `data/README.md` specifically calls out as a
discussion point: ~8% of rows (480 of 6,009) are missing it.

```python
orders = load_orders()
orders.isna().sum()
```
```
order_id             0
customer_id          0
product_id           0
order_date           0
quantity             0
unit_price           0
discount_pct       480
payment_method     180
shipping_region      0
status               0
order_total          0
dtype: int64
```

It's tempting to `fillna(0)` — "no discount recorded" sounds like "no discount applied."
But those aren't necessarily the same thing: a missing `discount_pct` might mean the
discount genuinely was 0, *or* it might mean the field wasn't recorded for some orders
regardless of the real discount. Filling blindly with 0 encodes an assumption you
haven't actually verified. Two more honest options:

1. **Fill with 0, but also keep a flag column** recording that it was originally
   missing, so downstream analysis (or a Module 4 model) can still tell the difference:
   ```python
   orders["discount_missing"] = orders["discount_pct"].isna()
   orders["discount_pct"] = orders["discount_pct"].fillna(0)
   ```
2. **Leave it as `NaN`** and let a later step (e.g. a scikit-learn imputer in Module 4)
   handle it explicitly and document the choice.

Either is defensible; silently guessing is not. This is exactly the kind of judgment
call real datasets force on you, and it's worth pausing on rather than reaching for
`.fillna(0)` on autopilot.

### Why this matters for ML later

Every scikit-learn model in Module 4 will simply crash on a `NaN` — `.fit()` raises a
`ValueError` if any feature column has missing values (a few tree-based
implementations, like some XGBoost configurations, are exceptions, but treat "models
need clean input" as the default assumption). That means every missing-data decision
you make here — drop this row, fill that column with a median, add a
`_missing` flag — becomes part of your model's behavior later, not just a cosmetic
cleanup step now.

**Full worked examples are in the notebook:**
`modules/03-pandas/notebooks/3.5-handling-missing-data.ipynb`

---

## Lesson 3.6 — Groupby and Aggregation

### The split-apply-combine idea

`.groupby()` implements a pattern you'll use constantly: **split** the data into groups
based on a column's values, **apply** an aggregation function to each group
independently, then **combine** the results back into one table. It's the pandas
equivalent of a spreadsheet pivot table's "group by category and sum" behavior.

We'll work with `orders`, deduplicated first (there's no reason to let the 5 duplicate
rows from Lesson 3.3/3.4 double-count into a summary table):

```python
orders = load_orders().drop_duplicates(subset=["order_id"])
```

### A single aggregation

```python
orders.groupby("status")["order_total"].mean().round(2)
```
```
status
cancelled    301.92
completed    272.78
returned     257.91
Name: order_total, dtype: float64
```

Read this as: "group all rows by `status`, then compute the mean of `order_total`
within each group." The result's index is the group labels (`cancelled`, `completed`,
`returned`) — a Series, since we selected one column. Interestingly, cancelled orders
have a *higher* average total than completed ones — a real pattern worth investigating
later, not an error.

### Multiple aggregations at once

`.agg()` with a list of function names applies each to the grouped column:

```python
orders.groupby("status")["order_total"].agg(["count", "mean", "sum"]).round(2)
```
```
           count    mean         sum
status                              
cancelled    192  301.92    57968.57
completed   5391  272.78  1470538.13
returned     421  257.91   108581.26
```

For readable output column names (and to aggregate *different* columns with different
functions in one call), use **named aggregation** — keyword arguments of the form
`new_column_name=("source_column", "function")`:

```python
summary = orders.groupby("status").agg(
    n_orders=("order_id", "count"),
    total_revenue=("order_total", "sum"),
    avg_order=("order_total", "mean"),
)
summary.round(2)
```
```
           n_orders  total_revenue  avg_order
status                                       
cancelled       192       57968.57     301.92
completed      5391     1470538.13     272.78
returned        421      108581.26     257.91
```

This named-aggregation form is worth reaching for by default — it's explicit about
which source column feeds which output, and it reads clearly even months later.

### Custom aggregation functions

Any function that takes a Series and returns a single value works with `.agg()`,
including one you write yourself:

```python
def value_range(s):
    return s.max() - s.min()

orders.groupby("payment_method")["order_total"].agg(value_range).round(2)
```
```
payment_method
bank_transfer    4099.94
credit_card      3304.64
gift_card        3073.24
paypal           3454.64
Name: order_total, dtype: float64
```

### Grouping by more than one column

Pass a list to `.groupby()` to split by the combination of several columns — the result
gets a **MultiIndex** (a hierarchical row index with one level per grouping column):

```python
orders.groupby(["status", "payment_method"])["order_total"].mean().round(2).head(6)
```
```
status     payment_method
cancelled  bank_transfer     349.49
           credit_card       266.40
           gift_card         310.11
           paypal            294.86
completed  bank_transfer     266.31
           credit_card       271.51
Name: order_total, dtype: float64
```

If a MultiIndex feels awkward to work with, `.reset_index()` flattens it back into
ordinary columns — useful right before writing a summary table to disk or plotting it:

```python
tidy = orders.groupby(["status", "payment_method"])["order_total"].mean().round(2).reset_index()
tidy.columns
```
```
Index(['status', 'payment_method', 'order_total'], dtype='object')
```

**Full worked examples are in the notebook:**
`modules/03-pandas/notebooks/3.6-groupby-and-aggregation.ipynb`

---

## Lesson 3.7 — Merge and Join Operations

### Why combine tables at all

The whole point of splitting the course dataset into three separate tables
(`customers`, `products`, `orders`) instead of one giant flat file is that each table
has one row per *thing* — one row per customer, one row per product, one row per order
— and a **foreign key** column (`customer_id` in `orders`, `product_id` in `orders`)
links them. This is the same idea as separate sheets in a workbook cross-referenced by
an ID column. `pd.merge()` is how you bring related columns from one table onto another.

```python
customers = load_customers()
orders = load_orders().drop_duplicates(subset=["order_id"])   # dedupe first, per Lesson 3.4
```

### The four join types, with real consequences

`pd.merge(left, right, on=key, how=...)` takes a `how=` that controls what happens when
a key on one side has no match on the other. `orders` and `customers` are a perfect
real example, because — as documented in `data/README.md` — **4 orders reference a
`customer_id` that doesn't exist in `customers.csv`** (`C90001`-`C90004`), on purpose.

**`how="inner"`** keeps only rows whose key matches on *both* sides — the orphan orders
disappear silently:

```python
inner = orders.merge(customers, on="customer_id", how="inner")
inner.shape
```
```
(6000, 17)
```

6,004 orders in, only 6,000 out — the 4 orphan rows vanished with no warning. That's the
danger of `how="inner"`: if you don't already know about the orphans, you'd never notice
you lost data.

**`how="left"`** keeps *every* row from `orders` (the "left" table), filling columns
from `customers` with `NaN` wherever there's no match:

```python
left = orders.merge(customers, on="customer_id", how="left")
left.shape
```
```
(6004, 17)
```

All 6,004 orders survive. The 4 orphan rows are still there, but now with `NaN` in every
customer column:

```python
orphans = left[left["signup_date"].isna()]
orphans[["order_id", "customer_id", "product_id", "order_total", "signup_date", "region"]]
```
```
     order_id customer_id product_id  order_total signup_date region
56    O006003      C90003      P0044        81.68         NaN    NaN
2166  O006004      C90004      P0020        24.94         NaN    NaN
2329  O006001      C90001      P0043        39.70         NaN    NaN
4531  O006002      C90002      P0009        61.94         NaN    NaN
```

That's the practical difference between `inner` and `left` in one real example:
`inner` quietly drops rows you might not know are gone; `left` keeps them and turns the
problem into unmistakable `NaN`s you can go find with `.isna()` — which is exactly why
`how="left"` is usually the safer default when you're merging in *reference* data (like
customer details) onto a table you don't want to shrink (like orders).

**`how="right"`** is the mirror image of `left` — keep every row from the *right* table
instead:

```python
right = customers.merge(orders, on="customer_id", how="right")
right.shape   # same 6,004 rows as `left`, just built by swapping which table is "left"
```

**`how="outer"`** keeps every row from *both* sides, matched where possible. Add
`indicator=True` to get a `_merge` column showing exactly where each row came from —
extremely useful for diagnosing exactly this kind of mismatch:

```python
outer = orders.merge(customers, on="customer_id", how="outer", indicator=True)
outer["_merge"].value_counts()
```
```
_merge
both          6000
right_only      69
left_only        4
```

This single table tells the whole story: 6,000 orders matched a real customer, 4 orders
are orphans (`left_only` — in `orders` but not `customers`), and 69 customers have never
placed an order at all (`right_only` — in `customers` but not `orders`). Running an
outer merge with `indicator=True` is a great first move whenever you're not sure how
clean two tables' keys are relative to each other.

### `.merge()` vs `.join()`

`.merge()` matches on column values (via `on=`). `.join()` matches on the **index**
instead — convenient when one side is already indexed by the key:

```python
customers_by_id = customers.set_index("customer_id")
orders_by_id = orders.head(3).set_index("customer_id")

orders_by_id.join(customers_by_id, how="left", lsuffix="_ord")[["order_id", "region"]]
```
```
            order_id region
customer_id                
C00258       O000080   west
C00559       O002751   WEST
C00126       O003297  NORTH
```

`lsuffix=`/`rsuffix=` disambiguate any column names that exist on both sides. In
practice, `.merge()` is far more common — reach for `.join()` mainly when both tables
are already indexed by the same key.

### Diagnosing common merge problems

**Duplicate keys inflate row counts.** If the *left* key has 3 matching rows on the
right, you get 3 output rows for it — a classic "why did my merge suddenly have way more
rows than I expected" bug. This is another reason to dedupe `orders` on `order_id`
*before* merging — a duplicate `order_id` merged against `products` would silently
double-count that order's revenue.

**Mismatched types silently produce zero matches.** If `customer_id` were stored as an
integer in one table and a string in the other, `pd.merge()` won't error — it will just
find no matches at all, and you'll get an unexpectedly empty (or all-`NaN`) result.
Always check `left["key"].dtype == right["key"].dtype` before merging if row counts
look wrong.

**A successful join doesn't guarantee the data means what you assumed.** `data/README.md`
notes that `orders["shipping_region"]` matches the customer's `region` only ~90% of the
time — the other 10% are legitimate (e.g. gifts shipped elsewhere), but if you assumed
"shipping region == customer region" while building a feature, a clean merge wouldn't
have warned you. Worth a quick sanity check any time a join "worked":

```python
combined = orders.merge(customers, on="customer_id", how="inner")
combined["region_clean"] = combined["region"].str.strip().str.lower().str.title()
(combined["shipping_region"] != combined["region_clean"]).mean().round(3)
```
```
0.112
```

About 11% mismatch — close to the ~10% `data/README.md` describes. (Try the comparison
against the *raw*, un-cleaned `region` column first, before reading on — you'll get a
wildly higher mismatch rate, because casing differences like `"west"` vs `"West"` count
as "different" too. That's a good reminder that a merge key matching correctly and a
downstream *comparison* being meaningful are two separate concerns — clean text columns
before comparing them, not just before joining on them.)

**Full worked examples — including the `inner` vs `left` orphan comparison above, run
yourself — are in the notebook:**
`modules/03-pandas/notebooks/3.7-merge-and-join.ipynb`

---

## Lesson 3.8 — Reshaping Data (Pivot/Melt)

### Wide vs. long

Data comes in two common shapes:

- **Long format**: one row per observation, with a column identifying *what* is being
  measured. `orders` is long — one row per order, with a `status` column, an
  `order_total` column, etc.
- **Wide format**: one row per entity, with separate *columns* for each category —
  easier for a human to scan, but harder to filter/group/plot with pandas' usual tools.

A summary table like "total revenue per membership tier, broken out by product
category" is naturally wide — tiers down the side, categories across the top. Long
format is what pandas (and most plotting/ML tools) actually want to operate on. Moving
between the two is a routine step in building reports.

### `.pivot_table()`: long → wide

First build a long table by merging orders with customer tier and product category:

```python
orders = load_orders().drop_duplicates(subset=["order_id"])
customers = load_customers()
products = load_products()

merged = orders.merge(customers[["customer_id", "membership_tier"]], on="customer_id", how="inner")
merged = merged.merge(products[["product_id", "category"]], on="product_id", how="inner")
merged[["order_id", "membership_tier", "category", "order_total"]].head(3)
```

Now pivot: rows (`index=`) become `membership_tier`, columns (`columns=`) become
`category`, cell values are the aggregated `order_total`:

```python
wide = merged.pivot_table(
    index="membership_tier",
    columns="category",
    values="order_total",
    aggfunc="sum",
)
wide.round(0)
```
```
category          Beauty    Books  Clothing  Electronics  Home & Kitchen  Sports & Outdoors
membership_tier                                                                            
Bronze           24699.0  24330.0   49835.0     379978.0         79900.0           128401.0
Gold              7162.0   6575.0   13567.0     115910.0         16687.0            49601.0
Platinum          3691.0   2904.0    6508.0      78220.0         11967.0            18350.0
Silver           19175.0  21406.0   45518.0     350013.0         69232.0           113251.0
```

This is `.groupby()` from Lesson 3.6 with an extra step: group by two columns, then
"unstack" one of them into the column axis instead of stacking it into a MultiIndex.
(In fact `.pivot_table()` is built on exactly that groupby-then-unstack machinery.)

`aggfunc=` accepts anything `.agg()` does — `"mean"`, `"count"`, a custom function, or a
dict mapping column to function for multiple `values=` columns at once. `fill_value=`
is worth knowing too, for combinations with no data (e.g. a month with zero cancelled
orders showing as 0 instead of `NaN`):

```python
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["month"] = orders["order_date"].dt.to_period("M").astype(str)
monthly = orders.pivot_table(
    index="month", columns="status", values="order_total", aggfunc="sum", fill_value=0
)
monthly.round(0).tail(6)
```
```
status   cancelled  completed  returned
month                                  
2025-01     3928.0    69049.0    2602.0
2025-02     3034.0    53511.0    2622.0
2025-03     4351.0    59843.0   10024.0
2025-04     2646.0    63603.0    3423.0
2025-05       95.0    63534.0    4656.0
2025-06     1004.0    74979.0    4677.0
```

### `.melt()`: wide → long

`.melt()` does the reverse: collapse several columns into two — one holding the old
column *names* (`var_name=`), one holding the old *values* (`value_name=`). It's what
you'd reach for to turn the `wide` pivot table back into a plotting- or
groupby-friendly long table:

```python
long = wide.reset_index().melt(
    id_vars="membership_tier",
    var_name="category",
    value_name="total_revenue",
)
long.head(8)
```
```
  membership_tier category  total_revenue
0          Bronze   Beauty       24698.65
1            Gold   Beauty        7162.46
2        Platinum   Beauty        3691.13
3          Silver   Beauty       19174.53
4          Bronze    Books       24329.55
5            Gold    Books        6575.23
6        Platinum    Books        2904.32
7          Silver    Books       21405.53
```

`wide` was 4 rows x 6 category columns; `id_vars="membership_tier"` keeps that column
fixed and melts the other 6 columns down, so `long` ends up 4 x 6 = 24 rows x 3 columns
— every (tier, category) combination gets its own row again, which is exactly the
`merged.groupby(["membership_tier", "category"])["order_total"].sum()` result you'd get
by skipping the pivot step entirely. `.pivot_table()` then `.melt()` is a round trip;
the reason to make the trip at all is that the *wide* shape in the middle is what a
human reads easily in a report, while the *long* shape on either end is what pandas,
matplotlib/seaborn, and scikit-learn all expect as input.

**Full worked examples are in the notebook:**
`modules/03-pandas/notebooks/3.8-reshaping-pivot-melt.ipynb`
