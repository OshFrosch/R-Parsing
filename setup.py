from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='rcrawler',
    version='',
    packages=['src', 'src.core', 'src.core.util', 'src.core.util.string_utils',
              'src.core.webhook', 'src.core.webhook.handlers',
              'src.core.downloader', 'src.core.ast_processing',
              'src.core.ast_processing.ast_classes', 'src.core.preprocessing',
              'src.core.preprocessing.preprocessor_class', 'test', 'test.core',
              'test.core.util'],
    ext_modules=cythonize(["src/core/ast_processing/ast_classes/*.pyx"],
                          annotate=True),
    include_dirs=[numpy.get_include()],
    url='',
    license='',
    author=['David Schwenke', 'Joshua Kraft'],
    author_email='schwenkedavid@t-online.de',
    description=''
)
