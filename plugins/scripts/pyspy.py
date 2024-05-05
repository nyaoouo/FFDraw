import pathlib
import os
import sys
from ff_draw.utils.requirements_ctrl import RequirementsCtrl


def main():
    RequirementsCtrl.auto_install_requirements('py-spy')
    executable = pathlib.Path(sys.executable).parent.joinpath('py-spy.exe')
    assert executable.exists(), f'py-spy not found: {executable}'
    os.system(f'start "" "{executable}" top --pid {os.getpid()}')

main()
