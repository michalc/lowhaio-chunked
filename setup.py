import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='lowhaio',
    version='0.0.0',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='Chunked transfer request encoding for lowhaio',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/lowhaio-chunked',
    py_modules=[
        'lowhaio_chunked',
    ],
    python_requires='>=3.6.3',
    install_requires=[
        'lowhaio',
    ],
    test_suite='test',
    tests_require=[
        'lowhaio==0.0.34',
        'aiohttp~=3.5.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
