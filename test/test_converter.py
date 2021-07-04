import pathlib
import subprocess


def test_template_existence() -> None:
    path = pathlib.Path("app/services/convert.py")
    cmd = ["python", str(path)]
    try:
        subprocess.check_output(cmd)
        actual = 1
    except subprocess.CalledProcessError as e:
        print(e.output)
        actual = 0
    finally:
        assert 1 == actual
