# Module 2: Python Programming Basics

This is your first real exposure to writing code, so we're going to go slowly and
explain every new word the first time it shows up. If you've never programmed before,
that's exactly who this module is for.

A quick note on how to read this: every gray box is a **code block**. Below many of
them you'll see either a `# ->` comment showing what a line prints, or a separate box
labeled "output" — that's what you'd see on your screen if you typed the code above it
into a notebook cell and ran it. You don't have to take our word for any of it — every
example here also lives in a runnable notebook (linked at the end of each section) where
you can run it yourself, change it, and see what happens.

---

## Lesson 2.1 — Variables, Types, and Operators

### What is a variable?

A **variable** is a name that points to a piece of data stored in the computer's memory.
Think of it like a labeled box: you put a value in the box, and from then on you can
refer to the value by the label instead of retyping it.

In Python, you create a variable with a single equals sign, `=`. This is called an
**assignment** — you are assigning a value to a name.

```python
age = 29
print(age)
# -> 29
```

Here `age` is the variable name and `29` is the value. `print()` is a built-in
**function** (a reusable piece of code) that displays a value on the screen — you'll see
it constantly throughout this course, since it's the easiest way to "look inside" your
program while it runs.

You can change what a variable points to at any time. This is called **reassignment**:

```python
age = 29
age = 30
print(age)
# -> 30
```

Nothing is "remembered" from the first assignment — the name `age` simply points to a
new value now. The old value `29` is gone (more precisely, Python cleans it up
automatically once nothing refers to it anymore).

You can also reassign a variable using its own current value, which is a very common
pattern:

```python
age = 29
age = age + 1
print(age)
# -> 30
```

Python evaluates the right-hand side of `=` first (`age + 1`, which is `30`), and only
then assigns that result to the name on the left. Because "take the current value, add
one, and store it back" is so common, Python has a shorthand for it:

```python
age = 29
age += 1   # same as: age = age + 1
print(age)
# -> 30
```

The same shorthand exists for `-=`, `*=`, `/=`, and more.

> **Beginner mistake: confusing `=` and `==`.**
> A single `=` **assigns** a value ("make `age` equal to 29"). A double `==` **compares**
> two values and gives back `True` or `False` ("is `age` equal to 29?"). Writing
> `if age = 30:` instead of `if age == 30:` is one of the most common beginner typos —
> and helpfully, Python will refuse to run it and show you a `SyntaxError` rather than
> silently doing the wrong thing.

### Naming variables

Variable names in Python:

- can contain letters, digits, and underscores (`_`), but **can't start with a digit**
- are **case-sensitive** — `Age` and `age` are two different variables
- can't be one of Python's reserved keywords (`if`, `for`, `class`, `return`, etc.)
- should, by convention, use `snake_case` — all lowercase, words separated by
  underscores, like `first_name` or `total_price`. This is the style you'll see
  throughout this course and throughout most Python code in the wild.

```python
first_name = "Grace"
_temp = 98.6
total_2024 = 150
```

Prefer descriptive names (`total_price` over `tp`) — you'll thank yourself later, and so
will anyone reading your code.

### Python's core types

Every value in Python has a **type**, which tells Python (and you) what kind of data it
is and what you can do with it. Module 2 mostly uses five core types:

| Type    | What it represents            | Example                |
|---------|-------------------------------|------------------------|
| `int`   | a whole number                | `29`, `-4`, `0`        |
| `float` | a number with a decimal point | `3.14`, `-0.5`, `29.0` |
| `str`   | text ("string")               | `"hello"`, `'Grace'`   |
| `bool`  | a truth value                 | `True`, `False`        |
| `None`  | "no value at all"             | `None`                 |

You can check any value's type with the built-in `type()` function:

```python
print(type(29))
print(type(3.14))
print(type("hello"))
print(type(True))
print(type(None))
```

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

**Strings** (`str`) are text, written between either single quotes `'...'` or double
quotes `"..."` — Python treats them identically, so pick one style and be consistent
(this course uses double quotes). You can glue strings together with `+`:

```python
first_name = "Ada"
last_name = "Lovelace"
full_name = first_name + " " + last_name
print(full_name)
# -> Ada Lovelace
```

A more readable way to build strings out of variables is an **f-string** (formatted
string) — put an `f` right before the opening quote, and any variable name inside `{}`
gets substituted in:

```python
first_name = "Ada"
age = 36
message = f"{first_name} is {age} years old."
print(message)
# -> Ada is 36 years old.
```

You'll use f-strings constantly — they're the standard, readable way to combine text and
values in modern Python.

**Booleans** (`bool`) have exactly two values, `True` and `False` (note the capital
letters — `true` and `false` are not valid Python). They represent yes/no, on/off,
did-this-happen/did-this-not-happen.

**`None`** is a special value that represents the *absence* of a value — "nothing here,"
as opposed to `0` or `""` (an empty string), which are real values that just happen to
be zero or empty. You'll see `None` used as a placeholder before a variable has a real
value, and as a function's way of saying "I have nothing to return."

### Dynamic typing

Python is **dynamically typed**, which means you never have to declare a variable's type
up front — Python figures it out from the value you assign, and a variable can point to
a completely different type later:

```python
data = 42
print(type(data))
# -> <class 'int'>

data = "now I'm text"
print(type(data))
# -> <class 'str'>
```

This is different from many other languages (Java, C++) where you must declare a
variable's type and it can never change. Dynamic typing makes Python fast to write and
forgiving to learn — but it also means Python won't catch a "wrong type" mistake for you
until the moment the bad line actually runs.

You can convert between types explicitly using `int()`, `float()`, `str()`, and
`bool()`:

```python
text_number = "42"
real_number = int(text_number)
print(real_number + 8)
# -> 50
```

```python
print(int("42"))      # -> 42
print(float("3.14"))  # -> 3.14
print(str(42))         # -> "42"
```

> **Beginner mistake: mixing strings and numbers.**
> `"42" + 8` raises a `TypeError: can only concatenate str (not "int") to str` — Python
> will not silently guess that you meant to add the numbers. If one side is a string and
> the other is a number, convert one of them first: `int("42") + 8` or
> `"42" + str(8)`.

### Operators

An **operator** is a symbol that performs an operation on one or more values.

**Arithmetic operators** work on numbers:

```python
print(7 + 3)    # addition       -> 10
print(7 - 3)    # subtraction    -> 4
print(7 * 3)    # multiplication -> 21
print(7 / 3)    # division       -> 2.3333333333333335
print(7 // 3)   # floor division -> 2   (division, rounded DOWN to a whole number)
print(7 % 3)    # modulo         -> 1   (the REMAINDER after division)
print(7 ** 2)   # exponent       -> 49  (7 to the power of 2)
```

Note that regular division `/` always returns a `float`, even when the numbers divide
evenly (`10 / 2` is `5.0`, not `5`). Floor division `//` and modulo `%` are especially
useful together — `//` tells you how many whole times one number fits into another, and
`%` tells you what's left over. For example, converting 130 minutes into hours and
minutes:

```python
total_minutes = 130
hours = total_minutes // 60
minutes = total_minutes % 60
print(f"{hours}h {minutes}m")
# -> 2h 10m
```

**Comparison operators** compare two values and always produce a `bool`:

```python
print(7 > 3)    # -> True   (greater than)
print(7 < 3)    # -> False  (less than)
print(7 >= 7)   # -> True   (greater than or equal to)
print(7 <= 3)   # -> False  (less than or equal to)
print(7 == 7)   # -> True   (equal to)
print(7 != 3)   # -> True   (not equal to)
```

**Boolean operators** combine or invert `bool` values: `and`, `or`, and `not`.

```python
age = 25
has_ticket = True

print(age >= 18 and has_ticket)  # -> True  (BOTH must be True)
print(age >= 65 or has_ticket)   # -> True  (at least ONE must be True)
print(not has_ticket)            # -> False (flips True <-> False)
```

`and` is `True` only when both sides are `True`. `or` is `True` when at least one side
is `True`. `not` flips a `bool` to its opposite.

> **Beginner mistake: off-by-one confusion with `>=` vs `>`.**
> "At least 18 years old" means `age >= 18`, not `age > 18` (which would incorrectly
> exclude someone who is exactly 18). Whenever a rule uses words like "at least," "at
> most," "no more than," or "up to," pause and check whether the boundary value itself
> should count — this exact mistake (called an **off-by-one error**) is one of the most
> common bugs in all of programming, and you'll meet it again with loops in Lesson 2.2.

Try it yourself: `notebooks/2.1-variables-types-operators.ipynb`

---

## Lesson 2.2 — Core Data Structures: Lists, Tuples, Dicts, Sets

So far every variable has held one single value. Python's built-in **data structures**
let a single variable hold *many* values, organized in different ways depending on what
you need.

### Lists

A **list** is an ordered, changeable ("mutable") collection of items, written with
square brackets `[]` and commas between items:

```python
groceries = ["eggs", "milk", "bread"]
print(groceries)
# -> ['eggs', 'milk', 'bread']
```

A list can hold any type, and even a mix of types, though in practice most lists hold
one consistent type of thing.

**Indexing** — get a single item by its position, starting from `0`:

```python
groceries = ["eggs", "milk", "bread"]
print(groceries[0])   # -> eggs   (the FIRST item)
print(groceries[1])   # -> milk
print(groceries[-1])  # -> bread  (the LAST item — negative indexes count from the end)
```

> **Beginner mistake: off-by-one errors with indexing.**
> Python counts positions starting at `0`, not `1`. In a 3-item list, the valid indexes
> are `0`, `1`, and `2` — there is no `groceries[3]`; trying it raises an
> `IndexError: list index out of range`. The *last* item's index is always
> `len(groceries) - 1`, or more simply, `groceries[-1]`.

**Slicing** — get a *sub-list* using `start:stop` (stop is excluded, same rule as
`range()`):

```python
numbers = [10, 20, 30, 40, 50]
print(numbers[1:3])   # -> [20, 30]   (index 1 up to, not including, index 3)
print(numbers[:2])    # -> [10, 20]   (from the start)
print(numbers[2:])    # -> [30, 40, 50]  (to the end)
```

**Mutating** a list — lists can be changed in place after creation:

```python
groceries = ["eggs", "milk", "bread"]
groceries.append("butter")        # add to the end
print(groceries)
# -> ['eggs', 'milk', 'bread', 'butter']

groceries[0] = "brown eggs"       # change an item by index
print(groceries)
# -> ['brown eggs', 'milk', 'bread', 'butter']

groceries.remove("bread")         # remove a specific value
print(groceries)
# -> ['brown eggs', 'milk', 'butter']

print(len(groceries))             # len() gives the number of items
# -> 3
```

Common list methods: `.append(x)` adds `x` to the end; `.remove(x)` removes the first
match of `x`; `.sort()` sorts the list in place; `.pop()` removes and returns the last
item. `len(some_list)` (a built-in function, not a method) tells you how many items are
in it.

### Tuples

A **tuple** looks and behaves almost exactly like a list — ordered, indexable, sliceable
— except it's **immutable**: once created, it cannot be changed.

```python
point = (3, 7)
print(point[0])
# -> 3
```

```python
point = (3, 7)
point[0] = 9
```

```text
TypeError: 'tuple' object does not support item assignment
```

**Why use a tuple instead of a list?** Reach for a tuple when the collection represents
a fixed, small group of values that shouldn't change — like an (x, y) coordinate, or a
(latitude, longitude) pair. The immutability is a *feature*: it signals to anyone reading
your code "this won't be modified," and Python will enforce that for you.

### Dictionaries

A **dictionary** (`dict`) stores **key/value pairs** — instead of looking items up by
position (like a list), you look them up by a meaningful key. Written with curly braces
`{}`:

```python
person = {"name": "Grace", "age": 36, "city": "Boston"}
print(person["name"])
# -> Grace
```

```python
person["age"] = 37                # update a value
person["job"] = "Engineer"        # add a new key/value pair
print(person)
# -> {'name': 'Grace', 'age': 37, 'city': 'Boston', 'job': 'Engineer'}
```

Looking up a key that doesn't exist raises a `KeyError`. To look up safely, with a
fallback value if the key is missing, use `.get()`:

```python
print(person.get("job"))              # -> Engineer
print(person.get("salary"))           # -> None  (key missing, no error)
print(person.get("salary", 0))        # -> 0     (custom default instead of None)
```

You can loop over a dictionary's keys, values, or both:

```python
person = {"name": "Grace", "age": 36}

for key in person:
    print(key)
# -> name
# -> age

for key, value in person.items():
    print(f"{key}: {value}")
# -> name: Grace
# -> age: 36
```

`.items()` gives you both the key and the value together on each pass — this is the
pattern you'll use most often.

### Sets

A **set** is an unordered collection of **unique** items — duplicates are automatically
removed, and there's no indexing (since there's no order to index into). Written with
curly braces like a dict, but with values only, no key/value pairs:

```python
tags = {"python", "beginner", "python", "tutorial"}
print(tags)
# -> {'python', 'beginner', 'tutorial'}   (the duplicate 'python' was dropped)
```

Sets exist for two main jobs: removing duplicates, and fast membership testing
(checking whether something is *in* the collection):

```python
unique_visitors = set(["alice", "bob", "alice", "carol", "bob"])
print(unique_visitors)
# -> {'alice', 'bob', 'carol'}

print("alice" in unique_visitors)
# -> True
print("dave" in unique_visitors)
# -> False
```

The `in` operator also works on lists, tuples, and dicts (checking dict keys), but a set
checks membership faster, which matters once a collection gets large.

### Which structure should I use?

| Structure | Ordered?              | Changeable? | Duplicates?         | Use it for                               |
|-----------|-----------------------|-------------|---------------------|------------------------------------------|
| `list`    | yes                   | yes         | yes                 | a general-purpose sequence you'll modify |
| `tuple`   | yes                   | no          | yes                 | a fixed, small group of values           |
| `dict`    | yes (insertion order) | yes         | keys must be unique | looking things up by name/key            |
| `set`     | no                    | yes         | no (auto-removed)   | uniqueness checks, membership tests      |

> **Beginner mistake: mutable default arguments.**
> This one is subtle enough that it trips up experienced programmers too, so we're
> flagging it early even though it involves functions (Lesson 2.4). Never write
> `def add_item(item, items=[]):` — that empty list `[]` is created **once**, when the
> function is defined, and then *reused and mutated* across every call, which leads to
> very confusing bugs. The fix is `def add_item(item, items=None):` and then
> `if items is None: items = []` inside the function body. We'll come back to this with
> a full example in Lesson 2.4.

Try it yourself: `notebooks/2.2-data-structures.ipynb`

---

## Lesson 2.3 — Control Flow

**Control flow** is how a program decides *which* code to run, and *how many times* to
run it, instead of just executing every line top to bottom. This lesson covers Python's
two tools for that: conditionals (`if`) and loops (`for` / `while`).

### `if` / `elif` / `else`

An `if` statement runs a block of code only when a condition is `True`:

```python
temperature = 85

if temperature > 80:
    print("It's hot outside.")
```

```text
It's hot outside.
```

Two things to notice, because both are essential Python syntax:

1. The line starts with `if`, followed by a condition, followed by a **colon** `:`.
2. The line(s) to run are **indented** — pushed in, conventionally by 4 spaces.

Python uses **indentation** (whitespace at the start of a line) to mark which lines
belong to which block of code, instead of curly braces `{}` like many other languages.
This is not a style choice you can skip — it's part of Python's syntax.

> **Beginner mistake: indentation errors.**
> Mixing tabs and spaces, or indenting inconsistently, causes an `IndentationError`. In
> a Jupyter notebook or any modern editor, pressing Tab reliably inserts spaces, so just
> be consistent — 4 spaces per indent level is the Python standard. If you copy-paste
> code from somewhere with different indentation, watch out.

Add `elif` (short for "else if") for additional conditions, and `else` to catch
everything that didn't match:

```python
temperature = 85

if temperature > 90:
    print("It's scorching.")
elif temperature > 70:
    print("It's warm.")
else:
    print("It's cool.")
```

```text
It's warm.
```

Python checks each condition top to bottom and runs the **first** block whose condition
is `True`, then skips the rest — even if a later condition would also have been `True`.
You can chain as many `elif`s as you need, and `else` (with no condition) is optional.

Conditions are usually built from the comparison and boolean operators from Lesson 2.1:

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("Entry allowed.")
else:
    print("Entry denied.")
```

```text
Entry allowed.
```

### `for` loops

A **loop** repeats a block of code multiple times. A `for` loop repeats once *for each
item* in a collection (like a list of names, or a range of numbers) — use it when you
know (or can get) the set of things you want to go through.

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

```text
apple
banana
cherry
```

On each pass through the loop, `fruit` takes on the next value from the list. You'll
learn much more about lists in Lesson 2.3 — for now, think of `["apple", "banana",
"cherry"]` as an ordered collection of three items.

To loop a specific number of times, use `range()`:

```python
for i in range(5):
    print(i)
```

```text
0
1
2
3
4
```

`range(5)` produces the numbers `0, 1, 2, 3, 4` — **five** numbers starting at `0`, and
stopping *before* `5`. This is the single most common source of off-by-one confusion for
beginners:

> **Beginner mistake: off-by-one errors with `range()`.**
> `range(5)` gives you `0` through `4`, **not** `1` through `5` — that's five numbers
> total, but the last one is `4`, not `5`. If you want the numbers `1` through `5`
> inclusive, write `range(1, 6)` (start at 1, stop *before* 6). Always double check
> which end of a `range()` is included when a bug seems to run "one too many" or "one
> too few" times.

`range()` can also take a start and a step: `range(2, 11, 2)` gives `2, 4, 6, 8, 10`.

### `while` loops

A `while` loop repeats as long as a condition stays `True` — use it when you *don't*
know in advance how many times you'll need to loop, only the condition that should stop
it.

```python
count = 0

while count < 3:
    print(count)
    count += 1
```

```text
0
1
2
```

Each time through the loop, Python checks the condition (`count < 3`) *before* running
the block. The moment it's `False`, the loop stops.

> **Beginner mistake: the infinite loop.**
> If you forget to update the variable the condition depends on (here, forgetting
> `count += 1`), the condition never becomes `False` and the loop runs forever, freezing
> your notebook. If a cell seems stuck, that's usually why — look for a `while` loop
> whose condition-variable never changes, and use the notebook's "stop" / interrupt
> button to break out of it.

**Rule of thumb:** reach for `for` when looping over a known collection or a fixed
number of times; reach for `while` when you're waiting for some condition to become
true and don't know how many iterations that will take.

### `break` and `continue`

`break` exits a loop immediately, skipping any remaining iterations:

```python
numbers = [4, 8, 15, 16, 23, 42]

for number in numbers:
    if number == 16:
        print("Found 16, stopping.")
        break
    print(number)
```

```text
4
8
15
Found 16, stopping.
```

`continue` skips the *rest of the current iteration* and jumps straight to the next one
(it does not exit the loop):

```python
for number in range(1, 6):
    if number % 2 == 0:
        continue   # skip even numbers
    print(number)
```

```text
1
3
5
```

### Common loop patterns: counting and accumulating

Two loop patterns come up constantly, so it's worth naming them explicitly.

**Counting** — keep a running tally of how many times something happens:

```python
words = ["cat", "dog", "cat", "bird", "cat"]
cat_count = 0

for word in words:
    if word == "cat":
        cat_count += 1

print(cat_count)
# -> 3
```

**Accumulating** — build up a total (or a combined result) across a loop:

```python
prices = [19.99, 5.50, 12.25]
total = 0

for price in prices:
    total += price

print(total)
# -> 37.74
```

Both patterns follow the same shape: create a starting variable *before* the loop
(`cat_count = 0`, `total = 0`), then update it *inside* the loop.

Try it yourself: `notebooks/2.3-control-flow.ipynb`

---

## Lesson 2.4 — Functions and Modules

### Why functions?

A **function** is a named, reusable block of code that you can run ("call") whenever you
need it, optionally feeding it inputs and getting a result back. Functions let you write
logic once and reuse it, instead of copy-pasting the same code everywhere.

You've already been *calling* functions — `print()`, `len()`, `type()`, `range()` are
all built-in functions. Now you'll learn to *define* your own.

```python
def greet(name):
    return f"Hello, {name}!"

message = greet("Ada")
print(message)
# -> Hello, Ada!
```

Breaking this down:

- `def` starts a function definition, followed by the function's name (`greet`),
  parentheses containing its **parameters**, and a colon.
- `name` is a **parameter** — a placeholder variable that receives whatever value is
  passed in when the function is called.
- The indented block is the function's **body** — the code that runs when it's called.
- `return` sends a value back out of the function to wherever it was called from.
- `greet("Ada")` is a function **call** — `"Ada"` here is called an **argument**, the
  actual value passed in for the `name` parameter.

A function that doesn't hit a `return` statement returns `None` automatically:

```python
def say_hi(name):
    print(f"Hi, {name}!")

result = say_hi("Ben")
# -> Hi, Ben!   (printed inside the function)
print(result)
# -> None        (say_hi never returned anything)
```

> **Beginner mistake: confusing `print()` and `return`.**
> `print()` only displays a value on screen — it doesn't hand the value back to the rest
> of your program. `return` is what actually makes a value available to whatever code
> called the function. A function that only `print()`s its result can't have that result
> stored in a variable or used in further calculations.

### Default parameter values

A parameter can have a **default value**, used automatically when the caller doesn't
supply that argument:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ada"))                  # -> Hello, Ada!
print(greet("Ada", "Good morning"))  # -> Good morning, Ada!
```

> **Beginner mistake: mutable default arguments.**
> As foreshadowed in Lesson 2.3 — default values are evaluated **once**, when the
> function is defined, not each time it's called. This is invisible with immutable
> defaults like `"Hello"` or `0`, but dangerous with a mutable default like a list:
>
> ```python
> def add_item(item, items=[]):
>     items.append(item)
>     return items
>
> print(add_item("apple"))    # -> ['apple']
> print(add_item("banana"))   # -> ['apple', 'banana']   <- surprise! same list reused
> ```
>
> Both calls share the *same* list object behind the scenes, because `[]` was only
> created once. The fix is to default to `None` and create a fresh list inside the
> function body:
>
> ```python
> def add_item(item, items=None):
>     if items is None:
>         items = []
>     items.append(item)
>     return items
>
> print(add_item("apple"))    # -> ['apple']
> print(add_item("banana"))   # -> ['banana']   <- correct, independent lists
> ```

### Multiple parameters and multiple return values

```python
def rectangle_area(width, height):
    return width * height

print(rectangle_area(4, 5))
# -> 20
```

A function can return more than one value at once, separated by commas — Python
packages them into a tuple:

```python
def min_and_max(numbers):
    return min(numbers), max(numbers)

low, high = min_and_max([4, 8, 15, 16, 23, 42])
print(low, high)
# -> 4 42
```

### Scope: local vs. global

**Scope** determines where in your code a variable name is visible. A variable created
*inside* a function is **local** to that function — it exists only while the function is
running, and it's invisible outside it:

```python
def calculate_total(prices):
    total = 0
    for price in prices:
        total += price
    return total

calculate_total([10, 20, 30])
print(total)
```

```text
NameError: name 'total' is not defined
```

`total` was created inside `calculate_total`, so it doesn't exist once the function
finishes — there's no `total` variable in the surrounding ("global") code at all.

A variable created *outside* any function, at the top level of your script or notebook,
is **global** — visible everywhere, including inside functions:

```python
tax_rate = 0.08   # global variable

def price_with_tax(price):
    return price * (1 + tax_rate)   # reads the global tax_rate

print(price_with_tax(100))
# -> 108.0
```

Functions can *read* a global variable freely, but by default, assigning to a name
inside a function creates a new **local** variable rather than changing the global one
— even if a global variable with the same name exists:

```python
counter = 0

def increment():
    counter = counter + 1   # this line fails
    return counter

increment()
```

```text
UnboundLocalError: cannot access local variable 'counter' where it is not associated
with a value
```

Python sees the assignment `counter = ...` inside the function and decides `counter` is
local to that function for its *entire* body — which means the `counter` on the
right-hand side refers to that not-yet-created local variable, not the global one. The
clean fix, in almost all cases, is to pass the value in and return the new value, rather
than reaching into global variables from inside a function:

```python
counter = 0

def increment(value):
    return value + 1

counter = increment(counter)
print(counter)
# -> 1
```

Keeping functions dependent only on their parameters (not on global variables) makes
them easier to test, reuse, and reason about — a good habit to build early.

### Modules and imports

A **module** is just a Python file (`.py`) whose functions and variables you can reuse
in another file with `import`. Python's **standard library** ships with many modules
ready to use:

```python
import math

print(math.sqrt(16))
# -> 4.0
print(math.pi)
# -> 3.141592653589793
```

`import math` makes everything inside the `math` module available under `math.`. Other
useful standard-library modules you'll meet soon: `random` (random numbers), `csv`
(reading/writing CSV files, Lesson 2.5), and `datetime` (dates and times).

You can also import your **own** files as modules. If you have a file `greetings.py`
sitting next to your notebook:

```python
# greetings.py
def say_hello(name):
    return f"Hello, {name}!"
```

...you can import and use it from a notebook in the same folder:

```python
from greetings import say_hello

print(say_hello("Ada"))
# -> Hello, Ada!
```

`from greetings import say_hello` pulls just the `say_hello` function out of
`greetings.py` directly into your namespace (so you call it as `say_hello(...)`, not
`greetings.say_hello(...)`). This is exactly the technique you'll use in the notebook for
this lesson — you'll write a tiny module and import it.

Try it yourself: `notebooks/2.4-functions-and-modules.ipynb`

---

## Lesson 2.5 — File I/O and Error Handling

### Reading and writing text files

**File I/O** ("input/output") means reading data from files on disk, or writing data out
to them. Python's built-in `open()` function is the standard way to do both.

The safest way to work with a file is with a `with` statement, which automatically
closes the file for you when you're done — even if something goes wrong partway through:

```python
with open("scratch/notes.txt", "w") as file:
    file.write("Hello, file!\n")
    file.write("This is line two.\n")
```

`"w"` here is the **mode** — `"w"` means "write" (create the file if it doesn't exist,
and **overwrite** it completely if it does). `as file` gives you a variable, `file`,
representing the open file while you're inside the `with` block.

Reading it back uses mode `"r"` ("read"):

```python
with open("scratch/notes.txt", "r") as file:
    contents = file.read()

print(contents)
```

```text
Hello, file!
This is line two.
```

To add to a file *without* erasing what's already there, use mode `"a"` ("append"):

```python
with open("scratch/notes.txt", "a") as file:
    file.write("This is line three.\n")
```

You can also loop over a file line by line, which is memory-efficient for large files:

```python
with open("scratch/notes.txt", "r") as file:
    for line in file:
        print(line.strip())   # .strip() removes the trailing newline character
```

### Reading and writing CSV files

A **CSV** file ("comma-separated values") is a plain text file storing tabular data —
rows and columns — with commas separating the values in each row. Python's built-in
`csv` module handles the fiddly details (like values that themselves contain commas) for
you:

```python
import csv

rows = [
    ["name", "score"],
    ["Ada", 95],
    ["Grace", 88],
]

with open("scratch/scores.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

The `newline=""` argument avoids extra blank lines being inserted on some systems — it's
boilerplate you'll always want when writing CSVs with this module.

Reading it back with `csv.DictReader` gives you each row as a dictionary keyed by the
header row, which is usually the most convenient form to work with:

```python
with open("scratch/scores.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
```

```text
{'name': 'Ada', 'score': '95'}
{'name': 'Grace', 'score': '88'}
```

Notice the scores came back as *strings* (`'95'`, not `95`) — every value read from a
CSV file starts out as text, and it's your job to convert (`int(row["score"])`) whatever
columns you plan to do arithmetic with. In Module 3 you'll use the `pandas` library,
which handles this conversion for you automatically — but it's worth seeing the manual,
built-in version first so you understand what's happening underneath.

### What is an exception?

An **exception** is Python's way of signaling that something went wrong while your
program was running — a file that doesn't exist, a division by zero, a type mismatch. By
default, an exception **stops your program** and prints a **traceback**, a message
showing what went wrong and where.

You've already seen several: `TypeError`, `IndexError`, `KeyError`, `NameError`. Here's
one more, `ZeroDivisionError`:

```python
print(10 / 0)
```

```text
ZeroDivisionError: division by zero
```

Exceptions exist so that problems are reported loudly and immediately, rather than
letting your program silently produce wrong answers.

### Handling errors with `try` / `except` / `finally`

Sometimes you *expect* an operation might fail, and you want your program to recover
gracefully instead of crashing. That's what `try` / `except` is for:

```python
try:
    result = 10 / 0
    print(result)
except ZeroDivisionError:
    print("Can't divide by zero!")
```

```text
Can't divide by zero!
```

Python runs the `try` block; if an exception matching `except ZeroDivisionError` occurs,
it jumps straight to that block instead of crashing, and the program continues normally
afterward.

You can catch multiple exception types, and access the error message itself:

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: cannot divide by zero.")
        return None
    except TypeError as error:
        print(f"Error: {error}")
        return None

print(safe_divide(10, 2))    # -> 5.0
print(safe_divide(10, 0))    # -> Error: cannot divide by zero. / None
print(safe_divide(10, "2"))  # -> Error: unsupported operand type(s) ... / None
```

`finally` adds a block that runs **no matter what** — whether the `try` block succeeded
or an exception was caught — which is useful for cleanup steps like closing a file:

```python
try:
    file = open("scratch/notes.txt", "r")
    contents = file.read()
finally:
    file.close()
    print("File closed.")
```

In practice, the `with` statement from earlier in this lesson already handles
closing files for you automatically, so you'll reach for explicit `finally` blocks less
often than `try`/`except` — but it's important to know it exists, since you'll see it in
other people's code.

> **Beginner mistake: catching every exception with a bare `except:`.**
> Writing `except:` with no exception type catches *everything*, including typos in your
> own code and `KeyboardInterrupt` (Ctrl+C) — this hides real bugs instead of fixing
> them. Always name the specific exception(s) you expect, like
> `except FileNotFoundError:`. If you genuinely aren't sure what might go wrong, catch
> the general `Exception` class by name (`except Exception as error:`) and print
> `error`, rather than silencing everything blindly.

A very common real pattern: trying to open a file that might not exist.

```python
try:
    with open("scratch/does_not_exist.txt", "r") as file:
        contents = file.read()
except FileNotFoundError:
    print("That file doesn't exist yet.")
```

```text
That file doesn't exist yet.
```

Try it yourself: `notebooks/2.5-file-io-and-error-handling.ipynb`

---

## Lesson 2.6 — A Light Introduction to Classes and Objects

### What is a class? What is an object?

Every value you've used so far — `29`, `"hello"`, `[1, 2, 3]` — is an **object**: a
bundle of data plus the operations that work on that data (a list "knows" how to
`.append()`; a string "knows" how to `.strip()`). A **class** is the *blueprint* used to
create objects of a particular kind. `int`, `str`, and `list` are all classes built into
Python — when you write `29`, you're creating an **instance** (a specific object) of the
`int` class.

You can define your own classes to model things specific to your own program — a
customer, a bank account, a machine learning model. Here's a small one:

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"
```

Breaking this down:

- `class Dog:` starts the class definition — `Dog` is the class name (by convention,
  class names use `CapitalizedWords`, unlike the `snake_case` used for variables and
  functions).
- `__init__` (short for "initialize") is a special method that runs automatically
  whenever you create a new `Dog` object. It's where you set up the object's initial
  data.
- `self` refers to "this particular object" — it's how a method reaches the data that
  belongs to the specific instance it was called on. It's always the first parameter of
  every method, and Python passes it in automatically — you never supply it yourself
  when calling the method.
- `self.name = name` stores `name` as an **attribute** on the object — data that lives
  on that specific instance and can be accessed later as `some_dog.name`.
- `bark` is a **method** — a function that belongs to the class and can use `self` to
  access that object's own data.

Creating (**instantiating**) and using an object:

```python
my_dog = Dog("Rex", "Labrador")
print(my_dog.name)
# -> Rex
print(my_dog.breed)
# -> Labrador
print(my_dog.bark())
# -> Rex says Woof!
```

`Dog("Rex", "Labrador")` calls `__init__` behind the scenes, with `self` automatically
set to the new object being created, `name` set to `"Rex"`, and `breed` set to
`"Labrador"`. Each `Dog` object you create is independent, with its own `name` and
`breed`:

```python
dog_a = Dog("Rex", "Labrador")
dog_b = Dog("Biscuit", "Poodle")

print(dog_a.bark())
# -> Rex says Woof!
print(dog_b.bark())
# -> Biscuit says Woof!
```

### Why does this matter for the rest of this course?

You won't be writing many classes of your own in this course — but you will be using
*other people's* classes constantly, and now their syntax will look familiar instead of
mysterious. In Module 4, you'll write code that looks like this:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()   # create an instance, just like Dog("Rex", "Labrador")
model.fit(x_train, y_train)  # call a method on it, just like my_dog.bark()
```

And in Module 5, PyTorch neural networks are *defined* using this exact pattern:

```python
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # set up layers here

    def forward(self, x):
        # define what happens when data flows through the network
        ...
```

You'll see this same `class ...: def __init__(self, ...):` pattern again when we build
scikit-learn pipelines and PyTorch models. Recognizing `__init__`, `self`, and "create an
object, then call methods on it" as a shape you've seen before will make both of those
modules much easier to follow, even though the internal details differ a lot.

> **Beginner mistake: forgetting `self`.**
> Every method inside a class must list `self` as its first parameter, even though you
> never pass it explicitly when calling the method — Python supplies it automatically.
> Forgetting it (`def bark():` instead of `def bark(self):`) causes a `TypeError` about
> the wrong number of arguments the moment you call `my_dog.bark()`, because Python is
> silently passing `my_dog` in as the first argument regardless.

Try it yourself: `notebooks/2.6-classes-and-objects.ipynb`
