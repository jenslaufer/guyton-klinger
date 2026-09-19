# guyton-klinger

A Streamlit calculator for the Guyton-Klinger guardrails withdrawal strategy.

Given a portfolio value and a desired starting withdrawal, it derives the initial
withdrawal rate, places an upper and a lower guardrail around it, and tells you
year by year whether to keep, cut or raise next year's withdrawal.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
python3 -m unittest discover -s tests -v
```

No dependencies beyond the standard library are needed for the tests — the decision
logic lives in a plain function, the Streamlit part only renders it.

## What this implements — and what it does not

Implemented is the guardrails core:

1. Raise last year's withdrawal by inflation.
2. Compare the resulting withdrawal rate against the current portfolio value.
3. Above the upper guardrail, cut by the adjustment step; below the lower guardrail,
   raise by it; in between, keep the inflation-adjusted figure.

Not implemented are two further rules of the original Guyton-Klinger paper:

- **Portfolio Management Rule** — skip the inflation raise after a year with a
  negative portfolio return.
- **Final-years exception** — the capital preservation rule is dropped in the last
  ~15 years of the plan.

So the numbers here are the guardrails reading, not the full Guyton-Klinger method.
