# Docstring Standard for Functions

This document defines the reproducible format for writing docstrings in Python functions, using the `detect_id_gap` function from [VSHC](https://github.com/Veicm/VSHC) as an example.

## Purpose

The docstring should:

- Clearly describe the function’s purpose.
- Specify assumptions or constraints.
- Provide a concise example of expected input and output.
- Describe all arguments with types and meaning.
- Specify the return type and meaning.

## Structure

### 1. Short Summary

- One line describing the primary purpose of the function.
- Written in imperative mood.

Example:

```python
Detect the first missing positive integer ID in a database table.
```

### 2. Extended Description (Optional)

- Provides context or assumptions.
- Explains any non-obvious behavior.

Example:

```python id="ghvtbv"
The function assumes that the ID column contains non-negative integers
(typically a PRIMARY KEY) and returns the first gap in ascending order.
```

### 3. Examples

- Show concrete examples of inputs and outputs.
- Use a Python-style code block.

Example:

```python id="5oiauq"
Example:
    IDs in table: [0, 1, 2, 4, 5]
    -> returns 3

    IDs in table: []
    -> returns 0
```

### 4. Arguments (Args)

- List all parameters in the order they appear in the function signature.
- Include:
  - Parameter name
  - Type in parentheses
  - Description (clear and concise)

- Use indentation for readability.

Example:

```python id="qf11mj"
Args:
    db_cursor (Cursor):
        An active SQLite database cursor.

    table_name (str):
        Name of the table to inspect.

    id_column (str):
        Name of the ID column. Defaults to "id".
```

### 5. Return Value (Returns)

- Specify the return type.
- Provide a description of what is returned.

Example:

```python id="m7fxmr"
Returns:
    int:
        The first missing integer ID.
```

### 6. Optional Notes (Optional)

- Can include:
  - Edge cases
  - Exceptions raised
  - Any additional context for maintainers

---

### Template for Reuse

```python id="zsan7i"
def function_name(param1: Type, param2: Type, ...) -> ReturnType:
    """
    One-line summary of the function.

    Optional extended description, including assumptions or constraints.

    Example:
        # Example usage
        input -> output

    Args:
        param1 (Type):
            Description of param1.
        param2 (Type):
            Description of param2.
        ...

    Returns:
        ReturnType:
            Description of what is returned.

    Optional notes:
        Additional clarifications or edge cases.
    """
```
