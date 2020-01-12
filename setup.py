from setuptools import setup


def main():
    setup(name='mpvyt',
          packages=['mpvyt'],
          entry_points={
              'console_scripts': [
                  'mpvyt = mpvyt.mpvyt:main'
              ]})


if __name__ == '__main__':
    main()
