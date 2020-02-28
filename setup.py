from setuptools import setup, find_packages

setup(
    name='crema',
    version='0.1',
    description='Kafka Library',
    url='https://github.com/paysense/crema',
    author='Rohit Laddha',
    author_email='rohit.laddha@paysense.in',
    packages=['crema'],
    zip_safe=False,
    packages=find_packages(),
)