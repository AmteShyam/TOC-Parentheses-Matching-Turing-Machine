# Parentheses Matching using a Turing Machine

CIA Activity - PCCO301 Theory of Computation, Sanjivani College of Engineering, Kopargaon
(Computer Engineering, TY Sem-I)

**Team:** Bharat Shelke (131), Shyam Amte (133), Vaibhav Dawange (134), Uday Gadekar (135)
**Course Incharge:** Dr. N. G. Pardeshi

## About
A deterministic, single-tape Turing Machine that decides whether a string over `{ ( , ) }`
has balanced parentheses. It repeatedly marks the leftmost unmatched `)` with `Y` and its
nearest unmatched `(` with `X`.

- States: `q0, q1, q2, qA, qR`
- Tape symbols: `( ) X Y _`
- Transitions: 13
- Time: O(n^2) (nested input takes 2(n+1)^2 steps, flat input 6n+2)
- Space: O(n)

## Run
```
python3 tm_parentheses.py
```
This prints step-by-step traces for `(())` and `())`, the 16 sample tests, an exhaustive
test of all strings of length 0-12, the step-count formulas, and then lets you type your own
strings.

## Files
- `tm_parentheses.py` - Turing Machine simulator and tests
- `TOC_REPORT` - the CIA report
