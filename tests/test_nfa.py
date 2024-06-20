from nfa_regex.nfa import NFA


def test_empty_string() -> None:
    nfa = NFA(
        alphabet={"a"},
        states={"a"},
        init_states={"a"},
        final_states={"a"},
        transitions={},
    )
    assert not nfa.accepts("a")
    assert nfa.accepts("")


def test_abc() -> None:
    nfa = NFA(
        alphabet={"a", "b", "c"},
        states={"init", "a", "b", "c"},
        init_states={"init"},
        final_states={"c"},
        transitions={
            ("init", "a"): {"a"},
            ("a", "b"): {"b"},
            ("b", "c"): {"c"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("a")
    assert not nfa.accepts("b")
    assert not nfa.accepts("c")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("abca")
    assert not nfa.accepts("abcc")
    assert nfa.accepts("abc")


def test_a_or_b_epsilon() -> None:
    nfa = NFA(
        alphabet={"a", "b"},
        states={"init", "a_init", "a", "b_init", "b"},
        init_states={"init"},
        final_states={"a", "b"},
        transitions={
            ("init", ""): {"a_init", "b_init"},
            ("a_init", "a"): {"a"},
            ("b_init", "b"): {"b"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("ba")
    assert not nfa.accepts("bb")
    assert not nfa.accepts("aa")
    assert nfa.accepts("a")
    assert nfa.accepts("b")


def test_a_or_b_multiple_init_states() -> None:
    nfa = NFA(
        alphabet={"a", "b"},
        states={"a_init", "a", "b_init", "b"},
        init_states={"a_init", "b_init"},
        final_states={"a", "b"},
        transitions={
            ("a_init", "a"): {"a"},
            ("b_init", "b"): {"b"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("aa")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("ba")
    assert not nfa.accepts("bb")
    assert nfa.accepts("a")
    assert nfa.accepts("b")


def test_ab_epsilon_edge() -> None:
    nfa = NFA(
        alphabet={"a", "b"},
        states={"init", "s0", "a", "s1", "b"},
        init_states={"init"},
        final_states={"b"},
        transitions={
            ("init", "a"): {"s0"},
            ("s0", ""): {"a"},
            ("a", "b"): {"s1"},
            ("s1", ""): {"b"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("a")
    assert not nfa.accepts("b")
    assert not nfa.accepts("aa")
    assert not nfa.accepts("ba")
    assert not nfa.accepts("bb")
    assert nfa.accepts("ab")


def test_epsilon_loop() -> None:
    nfa = NFA(
        alphabet={"a", "b"},
        states={"s0", "s1", "s2", "s3", "final"},
        init_states={"s0"},
        final_states={"final"},
        transitions={
            ("s0", ""): {"s1"},
            ("s1", ""): {"s2"},
            ("s2", ""): {"s3"},
            ("s3", ""): {"s0"},
            ("s3", "a"): {"final"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("b")
    assert not nfa.accepts("aa")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("ba")
    assert not nfa.accepts("bb")
    assert nfa.accepts("a")


def test_fork_join() -> None:
    nfa = NFA(
        alphabet={"a", "b", "c"},
        states={"init", "a", "b", "final"},
        init_states={"init"},
        final_states={"final"},
        transitions={
            ("init", "a"): {"a"},
            ("init", "b"): {"b"},
            ("a", "c"): {"final"},
            ("b", "c"): {"final"},
        },
    )
    assert not nfa.accepts("")
    assert not nfa.accepts("a")
    assert not nfa.accepts("b")
    assert not nfa.accepts("aca")
    assert not nfa.accepts("acb")
    assert not nfa.accepts("acc")
    assert nfa.accepts("ac")
    assert nfa.accepts("bc")


def test_abc_loop() -> None:
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
