"""Allow ``python -m tasks``."""

from tasks.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
