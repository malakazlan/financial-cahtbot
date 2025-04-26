from setuptools import setup, find_packages

setup(
    name="financial-chatbot",
    version="0.1",
    packages=find_packages(include=['recommendation', 'recommendation.*', 'nlp', 'nlp.*', 'data', 'data.*']),
    install_requires=[
        'scikit-learn>=1.0.0',
        'numpy>=1.20.0',
        'spacy>=3.0.0',
        'yfinance>=0.2.0',
        'pandas>=1.0.0',
    ],
) 