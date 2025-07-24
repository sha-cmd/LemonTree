from setuptools import setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='LemonTree',
    version='1.0',
    author='Romain BOYRIE',
    author_email='romain@boyrie.email',
    description='Presentation',
    url="https://github.com/sha-cmd/LemonTree",
    license='GNU V3 License',
    long_description=long_description,
    packages=['src'],
    install_requires=['pygame',],
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'prg = main'
        ]
    }
)
