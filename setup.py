from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='deployment-helper',
    version='0.1.0',
    packages=['changelog', 'helper'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'deployment-helper=helper:run'
        ]
    }
)
