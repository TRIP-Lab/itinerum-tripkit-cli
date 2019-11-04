from setuptools import setup

setup(
    name='itinerum-tripkit-cli',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'itinerum-tripkit==0.0.3',
    ],
    entry_points='''
        [console_scripts]
        tripkit-cli=tripkit_cli:main
    ''',
)
