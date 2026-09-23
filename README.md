# Data Science and Machine Learning Courses

A beginner-first data science / ML course, covering environment setup with `uv`,
Python fundamentals, numpy, pandas, matplotlib, and scikit-learn.

## Course outline

Each module is a folder under `tutorial/` with one Jupyter notebook per lesson.
Modules 3 to 5 work with the real Our World in Data CO2 emissions dataset in
`data/owid-co2-data.csv`.

| Module | Topic | Lessons |
| ------ | ----- | ------- |
| 1 | [Environment Setup](tutorial/01-environment-setup/) | 1.1 Starting a project with `uv` |
| 2 | [Python Basics](tutorial/02-python-basics/) | 2.1 Variables, types, operators · 2.2 Lists, tuples, dicts, sets · 2.3 Control flow · 2.4 Functions and modules · 2.5 File I/O and error handling · 2.6 Classes and objects |
| 3 | [pandas](tutorial/03-pandas/) | 3.1 Series and DataFrame basics · 3.2 Reading and writing data · 3.3 Selecting and filtering · 3.4 Rename, add, drop columns · 3.5 Handling missing data · 3.6 Groupby and aggregation · 3.7 Merge and join |
| 4 | [NumPy](tutorial/04-numpy/) | 4.1 Arrays basics · 4.2 Indexing, slicing, reshaping · 4.3 Math and statistics · 4.4 DataFrame and 2D array conversion |
| 5 | [matplotlib](tutorial/05-matplotlib/) | 5.1 Line plots of CO2 emissions |
| 6 | scikit-learn | Planned |

**Module 1 – Environment Setup.** Install VS Code, Python and `uv`, create a project
with a virtual environment, and run Jupyter. Slides live in `slides/`.

**Module 2 – Python Basics.** The core language needed for data work: variables and
types, built-in data structures, `if`/`for`/`while`, writing functions and importing
modules, reading and writing files with error handling, and a light look at classes.

**Module 3 – pandas.** Tabular data with `Series` and `DataFrame`: load CSV files,
inspect and select data with `.loc`/`.iloc` and boolean filters, reshape columns,
deal with missing values, summarise with `groupby`, and combine tables with `merge`.

**Module 4 – NumPy.** The array library underneath pandas: create arrays, index and
slice in 1D and 2D, boolean masks, `reshape`, element-wise math and broadcasting,
aggregations along an `axis`, `np.where`, and the round trip between a `DataFrame`
and a 2D array.

**Module 5 – matplotlib.** Visualise the CO2 dataset, starting with line plots of
per-capita emissions across countries.

**Module 6 – scikit-learn.** Introductory machine learning on the course dataset
(coming later).

## Start here

Download repo to local

```bash
git clone git@github.com:shuhua-wang/data-science-and-machine-learning-courses.git
```

Setup local venv:

```bash
cd data-science-and-machine-learning-courses
uv sync
```

Run jupyter lab:

```bash
uv run jupyter lab --allow-root
```

Slides:

```bash
make npm-install
make slides
```
