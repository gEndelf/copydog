from setuptools import setup
from copydog import __version__


requirements = open('requirements.txt').read().split('\n')

setup(
    name='copydog',
    version=__version__,
    packages=['copydog', 'copydog.api', 'copydog.utils'],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            'copydog = copydog.bin.runner:main'
    ]},
    url='http://copydog.readthedocs.org/',
    license='BSD',
    author='coagulant',
    author_email='baryshev@gmail.com',
    description='Copies issues between Redmine and Trello on the fly',
    long_description=open('README.rst').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    )
)
