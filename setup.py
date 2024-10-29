from cx_Freeze import setup, Executable

setup(
    name="Knee Injury Program",
    version="0.1.0",
    description="Knee Injury Research Program",
    executables=[Executable("main.py")]
)