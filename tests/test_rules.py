from nfa_regex.rules import (
    regex_alt,
    regex_char,
    regex_concat,
    regex_optional,
    regex_repeat,
)


def test_char() -> None:
    r = regex_char("c")
    assert not r.accepts("")
    assert not r.accepts("cc")
    assert not r.accepts("a")
    assert r.accepts("c")


def test_concat() -> None:
    r_a = regex_char("a")
    r_b = regex_char("b")
    r = regex_concat(r_a, r_b)
    assert not r.accepts("")
    assert not r.accepts("a")
    assert not r.accepts("aa")
    assert not r.accepts("b")
    assert not r.accepts("bb")
    assert not r.accepts("aba")
    assert not r.accepts("abb")
    assert r.accepts("ab")


def test_concat_concat() -> None:
    r_a = regex_char("a")
    r_b = regex_char("b")
    r = regex_concat(r_a, r_b)
    r = regex_concat(r, r)
    assert not r.accepts("")
    assert not r.accepts("ab")
    assert not r.accepts("ababab")
    assert r.accepts("abab")


def test_optional() -> None:
    r_a = regex_char("a")
    r = regex_optional(r_a)
    assert not r.accepts("aa")
    assert not r.accepts("b")
    assert r.accepts("")
    assert r.accepts("a")


def test_multiple_optional() -> None:
    r_a = regex_char("a")
    r = regex_optional(regex_optional(regex_optional(r_a)))
    assert not r.accepts("aa")
    assert not r.accepts("b")
    assert r.accepts("")
    assert r.accepts("a")


def test_optional_concat() -> None:
    r_a = regex_optional(regex_char("a"))
    r_b = regex_char("b")
    r = regex_concat(r_a, r_b)
    assert not r.accepts("")
    assert not r.accepts("a")
    assert not r.accepts("aba")
    assert not r.accepts("ba")
    assert not r.accepts("abb")
    assert r.accepts("ab")
    assert r.accepts("b")


def test_repeat() -> None:
    r_a = regex_char("a")
    r = regex_repeat(r_a)
    assert not r.accepts("ab")
    assert not r.accepts("aba")
    assert not r.accepts("ba")
    assert not r.accepts("abb")
    assert r.accepts("")
    assert r.accepts("a")
    assert r.accepts("aa")
    assert r.accepts("aaa")
    assert r.accepts("aaaa")


def test_repeat_twice() -> None:
    r_a = regex_char("a")
    r = regex_repeat(regex_repeat(r_a))
    assert not r.accepts("ab")
    assert not r.accepts("aba")
    assert not r.accepts("ba")
    assert not r.accepts("abb")
    assert r.accepts("")
    assert r.accepts("a")
    assert r.accepts("aa")
    assert r.accepts("aaa")
    assert r.accepts("aaaa")


def test_concat_repeat() -> None:
    r_a = regex_repeat(regex_char("a"))
    r_b = regex_char("b")
    r_ab = regex_concat(r_a, r_b)
    r = regex_repeat(r_ab)
    assert not r.accepts("ba")
    assert not r.accepts("baa")
    assert not r.accepts("aba")
    assert r.accepts("")
    assert r.accepts("b")
    assert r.accepts("bb")
    assert r.accepts("bb")
    assert r.accepts("ab")
    assert r.accepts("abab")
    assert r.accepts("ababab")
    assert r.accepts("aaab")
    assert r.accepts("aaabb")
    assert r.accepts("aaabab")
    assert r.accepts("aaabaaaab")
    assert r.accepts("bbbbbbbbb")


def test_alt() -> None:
    r_a = regex_char("a")
    r_b = regex_char("b")

    r_ab = regex_concat(r_a, r_b)
    r_bab = regex_concat(regex_concat(r_b, r_a), r_b)

    r = regex_alt(r_ab, r_bab)

    assert not r.accepts("")
    assert not r.accepts("a")
    assert not r.accepts("aa")
    assert not r.accepts("abb")
    assert not r.accepts("b")
    assert not r.accepts("ba")
    assert not r.accepts("baba")
    assert not r.accepts("babb")
    assert r.accepts("ab")
    assert r.accepts("bab")


def test_complex() -> None:
    r_a = regex_char("a")
    r_b = regex_char("b")
    r_c = regex_char("c")

    r_ab = regex_concat(r_a, r_b)
    r_cab = regex_concat(r_c, regex_concat(regex_optional(r_a), r_b))

    r_alt = regex_alt(r_ab, r_cab)
    r = regex_repeat(r_alt)

    assert not r.accepts("a")
    assert not r.accepts("b")
    assert not r.accepts("c")
    assert not r.accepts("cba")
    assert not r.accepts("abc")
    assert not r.accepts("ababa")
    assert not r.accepts("caab")
    assert r.accepts("")
    assert r.accepts("ab")
    assert r.accepts("abab")
    assert r.accepts("abcb")
    assert r.accepts("cb")
    assert r.accepts("cbab")
    assert r.accepts("abcab")
    assert r.accepts("cabab")
    assert r.accepts("abcabab")
    assert r.accepts("abcabcabababcababcbababababcb")
