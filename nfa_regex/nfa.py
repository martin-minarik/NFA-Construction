from typing import Dict, Set, Tuple

NFATransitions = Dict[Tuple[str, str], Set[str]]


class NFA:
    def __init__(
        self,
        alphabet: Set[str],
        states: Set[str],
        init_states: Set[str],
        final_states: Set[str],
        transitions: NFATransitions,
    ):
        assert len(alphabet) > 0
        for c in alphabet:
            assert len(c) == 1

        assert len(init_states) > 0
        for state in init_states:
            assert state in states

        assert len(states) > 0
        for state in final_states:
            assert state in states
        for (state, c), targets in transitions.items():
            assert c in alphabet or c == ""

            for target in targets:
                assert target in states

        self.alphabet = alphabet
        self.states = states
        self.final_states = final_states
        self.transitions = transitions
        self.init_states = init_states

    def accepts(self, input_: str) -> bool:
        current_states = self.init_states
        current_states = self.include_states_reached_by_epsilon(current_states)

        for char in input_:
            current_states = self.get_next_states_by(current_states, char)
            current_states = self.include_states_reached_by_epsilon(current_states)

        return bool(current_states.intersection(self.final_states))

    def get_next_states_by(self, current_states: Set[str], char: str) -> Set[str]:
        next_states = set()
        for state in current_states:
            if next_states_by_char := self.transitions.get((state, char), set()):
                next_states.update(next_states_by_char)

        return next_states

    def include_states_reached_by_epsilon(self, current_states: Set[str]) -> Set[str]:
        next_states = current_states.copy()
        checked_states = set()

        while True:
            flag = False
            for state in next_states.copy():
                if state in checked_states:
                    continue

                if states_reached_by_epsilon := self.transitions.get(
                    (state, ""), set()
                ):
                    next_states.update(states_reached_by_epsilon)
                    flag = True

                checked_states.add(state)

            if not flag:
                break

        return next_states

    def __or__(self, other: "NFA") -> "NFA":
        new_states = {f"{state}_a" for state in self.states}
        new_states |= {f"{state}_b" for state in other.states}

        new_init_states = {f"{state}_a" for state in self.init_states}
        new_init_states |= {f"{state}_b" for state in other.init_states}

        new_final_states = {f"{state}_a" for state in self.final_states}
        new_final_states |= {f"{state}_b" for state in other.final_states}

        new_transitions = {
            (f"{state}_a", char): {f"{next_state}_a" for next_state in next_states}
            for (state, char), next_states in self.transitions.items()
        }

        new_transitions |= {
            (f"{state}_b", char): {f"{next_state}_b" for next_state in next_states}
            for (state, char), next_states in other.transitions.items()
        }

        return NFA(
            alphabet=self.alphabet | other.alphabet,
            states=new_states,
            init_states=new_init_states,
            final_states=new_final_states,
            transitions=new_transitions,
        )

    def __add__(self, other: "NFA") -> "NFA":
        new_nfa = self | other
        new_nfa.init_states = {f"{state}_a" for state in self.init_states}
        new_nfa.final_states = {f"{state}_b" for state in other.final_states}

        for final_state_a in self.final_states:
            for init_state_b in other.init_states:
                new_nfa.transitions.setdefault((f"{final_state_a}_a", ""), set()).add(
                    f"{init_state_b}_b"
                )

        return new_nfa

    def add_suffix_if_exists(self, state_name: str) -> str:
        counter = 1
        while state_name in self.states:
            state_name = f"{state_name}({counter})"
            counter += 1
        return state_name
