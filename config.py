# Use it when first use project firstly on this machine
import subprocess
import sys


def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
    packages_to_install = [
        "requests",
        "numpy",
        "pandas",
        "matplotlib",
        "cx_Freeze",
        "scipy",
    ]

    print("Package installation initialized...")
    install_packages(packages_to_install)
    print("Installation completed!")
