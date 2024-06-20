from copy import deepcopy

from .nfa import NFA


def regex_char(char: str) -> NFA:
    return NFA(
        alphabet=set(char),
        states={"init", "match"},
        init_states={"init"},
        final_states={"match"},
        transitions={
            ("init", char): {"match"},
        },
    )


def regex_concat(a: NFA, b: NFA) -> NFA:
    return a + b


def regex_optional(nfa: NFA) -> NFA:
    new_nfa = deepcopy(nfa)
    new_nfa.final_states |= nfa.init_states
    return new_nfa


def regex_repeat(nfa: NFA) -> NFA:
    new_nfa = deepcopy(nfa)
    for final_state in new_nfa.final_states:
        for init_state in new_nfa.init_states:
            new_nfa.transitions.setdefault((final_state, ""), set()).add(init_state)

    iter_state = new_nfa.add_suffix_if_exists("iter")
    new_nfa.states.add(iter_state)
    new_nfa.final_states.add(iter_state)
    new_nfa.transitions[(iter_state, "")] = new_nfa.init_states.copy()
    new_nfa.init_states = {iter_state}
    return new_nfa


def regex_alt(a: NFA, b: NFA) -> NFA:
    return a | b
