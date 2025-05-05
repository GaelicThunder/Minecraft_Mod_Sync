from setuptools import setup

setup(
    name='mcmodsync',
    version='1.0',
    py_modules=['cli'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'mcmodsync=cli:main'
        ]
    }
)
