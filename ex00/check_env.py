import importlib
import platform
import sys


REQUIRED_PYTHON = (3, 9)
LIBRARIES = ("pandas", "numpy", "jupyter", "plotly")


def version_for(module_name: str) -> str:
    module = importlib.import_module(module_name)
    return getattr(module, "__version__", "version attribute is not exposed")


def main() -> None:
    print(f"Python: {platform.python_version()}")
    if sys.version_info < REQUIRED_PYTHON:
        raise RuntimeError("Python 3.9+ is required")

    print("Required libraries:")
    for module_name in LIBRARIES:
        print(f"- {module_name}: {version_for(module_name)}")


if __name__ == "__main__":
    main()
