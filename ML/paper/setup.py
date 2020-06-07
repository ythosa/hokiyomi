from setuptools import setup

setup(
    name="paper",
    version='0.1',
    py_modules=[],
    install_requires=[
        'Click',
        'pillow'
    ],
    entry_points='''
        [console_scripts]
        paper=main:cli
    ''',
)