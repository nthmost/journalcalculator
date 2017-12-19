from setuptools import setup, find_packages

setup(
    name = "journalcalculator",
    version = "0.1",
    description = "JournalCalculator.com",
    url="http://journalcalculator.com",
    author = "Naomi Most",
    author_email = "naomi@nthmost.com",
    maintainer = "Naomi Most",
    maintainer_email = "naomi@nthmost.com",
    license = "Apache 2.0",
    zip_safe = False,
    packages = find_packages(),
    install_requires = [ 
                         "flask",
                         "pytz",
                         "pyrfc3339",
                         "configparser",
                         "gunicorn",
                         "fabric",
                         "metapub",
                        ],
    )
