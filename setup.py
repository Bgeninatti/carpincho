import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carpincho",
    version="0.0.1",
    author="Bruno Geninatti",
    author_email="bruno.geninatti@ac.python.org.ar",
    description="Bot para la registracion de PyConAr 2021",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bgeninatti/carpincho",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'lxml',
        'discord.py',
        'click',
        'peewee',
        'psycopg2',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'carpincho=carpincho.cli:main',
        ],
    },
)
