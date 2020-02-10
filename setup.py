from setuptools import setup

setup(
    name='mpvyt',
    packages=['mpvyt'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'mpvyt = mpvyt.mpvyt:main'
        ]
    }
)
