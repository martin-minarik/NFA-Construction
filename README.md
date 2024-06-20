# NFA Construction

This project is a Python implementation of a simplified version of Thompson's construction algorithm.

It constructs **NFA** (nondeterministic finite automata) by chaining rules.


## Project Structure

The project consists of two main Python files:

- `nfa_regex/nfa.py`: Defines the `NFA` class, which represents a nondeterministic finite automaton.
- `nfa_regex/rules.py`: Contains the functions for constructing an NFA from a regular expression.

## Example

- NFA

```python
from nfa_regex.nfa import NFA

nfa = NFA(
    alphabet={"a", "b", "c"},
    states={"init", "a", "b"},
    init_states={"init"},
    final_states={"init"},
    transitions={
        ("init", "a"): {"a"},
        ("a", "b"): {"b"},
        ("b", "c"): {"init"},
    },
)

assert not nfa.accepts("a")
assert not nfa.accepts("b")
assert not nfa.accepts("ab")
assert not nfa.accepts("abca")
assert nfa.accepts("")
assert nfa.accepts("abc")
assert nfa.accepts("abcabc")
assert nfa.accepts("abcabcabc")
assert nfa.accepts("abcabcabcabc")
```

- regex rules

```python
from nfa_regex.rules import *

r_a = regex_char("a")  # equals r"a"
r_b = regex_char("b")  # equals r"b"
r_c = regex_char("c")  # equals r"c"

r_ab = regex_concat(r_a, r_b)  # equals r"ab"
r_cab = regex_concat(r_c, regex_concat(regex_optional(r_a), r_b))  # equals r"ca?b"

r_alt = regex_alt(r_ab, r_cab)  # equals r"ab|ca?b"
r = regex_repeat(r_alt)  # equals r"(ab|ca?b)*"

assert not r.accepts("a")  # False
assert not r.accepts("b")  # False
assert not r.accepts("c")  # False
assert not r.accepts("cba")  # False
assert not r.accepts("abc")  # False
assert not r.accepts("ababa")  # False
assert not r.accepts("caab")  # False
assert r.accepts("")  # True
assert r.accepts("ab")  # True
assert r.accepts("abab")  # True
assert r.accepts("abcb")  # True
assert r.accepts("cb")  # True
assert r.accepts("cbab")  # True
assert r.accepts("abcab")  # True
assert r.accepts("cabab")  # True
assert r.accepts("abcabab")  # True
assert r.accepts("abcabcabababcababcbababababcb")  # True
```
