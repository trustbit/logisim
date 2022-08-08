from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

install_requires = ["fire", "pandas", "numpy"]
setup(
    name="logisim",
    version="1.0.0",
    author="Rinat Abdullin",
    author_email="rinat.abdullin@trustbit.tech",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/trustbit/logisim",
    license="LICENSE.txt",
    description="Logistic Simulation Companion for the blog post series",
    long_description=(this_directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",  # Optional (see note above)
    python_requires=">=3.9, <4",
    install_requires=install_requires,
    project_urls={  # Optional
        "Github": "https://github.com/trustbit/logisim",
    },
    entry_points={  # Optional
        "console_scripts": [
            "logisim2=logisim2.main:main",
            "logisim3=logisim3.main:main"
        ],
    },
    zip_safe=False,
    include_package_data=True,
)
