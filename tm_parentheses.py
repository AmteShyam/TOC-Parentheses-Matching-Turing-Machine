"""
Parentheses Matching using a Turing Machine
Course: PCCO301 - Theory of Computation (CIA Activity)

A deterministic single-tape Turing Machine that decides whether a string
over {(, )} is balanced. It uses marking symbols:
    Y  -> overwrites a matched closing parenthesis
    X  -> overwrites a matched opening parenthesis

States: q0 (scan right), q1 (return left), q2 (final check),
        qA (accept), qR (reject)
"""

import itertools

BLANK = '_'

# DELTA[(state, symbol)] = (write, move, next_state)   -- 13 transitions
DELTA = {
    ('q0', '('): ('(', 'R', 'q0'),    # 1  skip opening parenthesis
    ('q0', 'X'): ('X', 'R', 'q0'),    # 2  skip matched opening
    ('q0', 'Y'): ('Y', 'R', 'q0'),    # 3  skip matched closing
    ('q0', ')'): ('Y', 'L', 'q1'),    # 4  mark closing, look for partner
    ('q0', BLANK): (BLANK, 'L', 'q2'),  # 5  right end reached, check
    ('q1', 'X'): ('X', 'L', 'q1'),    # 6  skip matched opening
    ('q1', 'Y'): ('Y', 'L', 'q1'),    # 7  skip matched closing
    ('q1', '('): ('X', 'R', 'q0'),    # 8  mark partner, resume scan
    ('q1', BLANK): (BLANK, 'R', 'qR'),  # 9  no partner: reject
    ('q2', 'X'): ('X', 'L', 'q2'),    # 10 skip matched opening
    ('q2', 'Y'): ('Y', 'L', 'q2'),    # 11 skip matched closing
    ('q2', '('): ('(', 'R', 'qR'),    # 12 unmatched ( found: reject
    ('q2', BLANK): (BLANK, 'R', 'qA'),  # 13 all matched: accept
}


def show_tape(tape, head):
    return ' '.join(f'[{c}]' if i == head else c for i, c in enumerate(tape))


def run(text, trace=False):
    """Run the TM on `text`. Returns (accepted, steps)."""
    tape = [BLANK] + list(text) + [BLANK]
    head, state, steps = 1, 'q0', 0
    if trace:
        print(f"{'Step':<5}{'State':<6}{'Pos':<5}{'Read':<5}{'Write':<6}"
              f"{'Move':<5}{'Next':<5}Tape before step")
    while state not in ('qA', 'qR'):
        symbol = tape[head]
        if (state, symbol) not in DELTA:          # illegal symbol
            state = 'qR'
            break
        write, move, nxt = DELTA[(state, symbol)]
        if trace:
            print(f"{steps + 1:<5}{state:<6}{head - 1:<5}{symbol:<5}{write:<6}"
                  f"{move:<5}{nxt:<5}{show_tape(tape, head)}")
        tape[head] = write                        # tape marking
        head += 1 if move == 'R' else -1          # head movement
        state = nxt                               # state transition
        steps += 1
        if head < 0:                              # extend tape on the left
            tape.insert(0, BLANK)
            head = 0
        elif head >= len(tape):                   # extend tape on the right
            tape.append(BLANK)
    return state == 'qA', steps


def reference(text):
    """Independent checker: counts nesting depth."""
    depth = 0
    for c in text:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0:
                return False
        else:
            return False
    return depth == 0


def sample_tests():
    cases = ["", "()", "(())", "()()", "(()())", "((()))", "(()(()))",
             "()(())()", "(", ")", ")(", "(()", "())", "())(", "((())",
             "(()))("]
    print("\nSample tests")
    print(f"{'Input':<12}{'Expected':<14}{'TM output':<11}{'Steps':<7}Result")
    for s in cases:
        ok, steps = run(s)
        exp = reference(s)
        print(f"{s or 'e (empty)':<12}{'Balanced' if exp else 'Not balanced':<14}"
              f"{'ACCEPT' if ok else 'REJECT':<11}{steps:<7}"
              f"{'Pass' if ok == exp else 'FAIL'}")


def exhaustive_test(max_len=12):
    total = mismatches = accepted = 0
    for L in range(max_len + 1):
        for p in itertools.product('()', repeat=L):
            s = ''.join(p)
            ok, _ = run(s)
            total += 1
            accepted += ok
            mismatches += ok != reference(s)
    print(f"\nExhaustive test, length 0..{max_len}: {total} strings, "
          f"{accepted} accepted, {mismatches} mismatches")


def complexity():
    print("\nStep counts (n pairs)")
    print(f"{'n':<5}{'nested':<10}{'2(n+1)^2':<10}{'flat':<8}6n+2")
    for n in (1, 2, 5, 10, 30, 60):
        nested = run('(' * n + ')' * n)[1]
        flat = run('()' * n)[1]
        print(f"{n:<5}{nested:<10}{2 * (n + 1) ** 2:<10}{flat:<8}{6 * n + 2}")


if __name__ == '__main__':
    print("Trace for input (())")
    print(run("(())", trace=True))
    print("\nTrace for input ())")
    print(run("())", trace=True))
    sample_tests()
    exhaustive_test(12)
    complexity()
    while True:
        try:
            s = input("\nEnter a parentheses string (blank to quit): ").strip()
        except EOFError:
            break
        if not s:
            break
        ok, steps = run(s, trace=True)
        print("ACCEPT (balanced)" if ok else "REJECT (not balanced)", f"- {steps} steps")
