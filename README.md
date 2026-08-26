# Week 1 — Hello, Model

Starter files for the first lab of COMP840/COMP740: three short scripts that
make your first calls to a language model, plus a shared helper module.

| File                   | What it shows                                          |
|------------------------|---------------------------------------------------------|
| `hello_1_call.py`      | The basics: one prompt, one answer                     |
| `hello_2_variance.py`  | The same prompt gives different answers (non-determinism) |
| `hello_3_cost.py`      | Reading token counts and estimating cost at scale       |

`config.py` and `llm.py` are shared by every lab this term — read `llm.py`
once, but you won't need to edit it. `doctor.py` checks that your setup is
correct.

## Setup

1. Create and activate a virtual environment:

   **Windows:**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   **Mac:**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your API key:

   Copy `.env.example` to `.env` and paste in your real key.

   **Windows:** `copy .env.example .env`
   **Mac:** `cp .env.example .env`

   Edit `.env` in a code editor (not Notepad) so it reads:
   ```
   GEMINI_API_KEY=AIza...your real key...
   ```
   `.env` is already listed in `.gitignore` — never commit it.

4. Verify everything works:
   ```
   python doctor.py       (Windows)
   python3 doctor.py      (Mac)
   ```
   Every line should say `PASS`.

## Running the labs

```
python hello_1_call.py       (Windows)
python3 hello_1_call.py      (Mac)
```
Then `hello_2_variance.py`, then `hello_3_cost.py`, the same way.

## Submitting

Fill in `OUTPUT.md` with what you observed for each script, commit your
work, and push to this repository. Add your instructor as a collaborator
under Settings → Collaborators so your work can be reviewed.
