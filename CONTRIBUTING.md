# Contributing to World Meeting Card

Start with the [usage example](README.md). For a bug report, include a minimal synthetic input, the expected result and the observed result.

## Run the checks

Use Python 3.12 or newer from the repository root.

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/check.py
```

Add a regression case to the included check when changing an input format, calculation, or output.
