from shutil import which


def ensure_pandoc_available() -> str:
    pandoc = which("pandoc")

    if pandoc is None:
        raise PandocNotFoundError(
            "Pandoc was not found in the system PATH."
        )

    return pandoc


class PandocNotFoundError(Exception):
    pass