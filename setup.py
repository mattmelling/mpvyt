from setuptools import setup


def main():
    setup(name='mpvyt',
          packages=['mpvyt'],
          install_requires=[
              'requests',
              'beautifulsoup4',
              'lxml'
          ])


if __name__ == '__main__':
    main()
