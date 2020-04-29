from setuptools import setup, find_packages

setup(
    name='crema',
    version='0.10',
    description='Kafka Library',
    url='https://github.com/paysense/crema',
    author='Rohit Laddha',
    author_email='rohit.laddha@paysense.in',
    packages=['crema'],
    zip_safe=False,
    install_requires=['kafka-python==1.4.7', 'uhashring==1.1']
)
