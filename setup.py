import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='redash-stmo',
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'dockerflow>=2018.4.0',
        'requests',
        'sqlparse',
        'six',
        'pyhive',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    description="Extensions to Redash by Mozilla",
    long_description=read('README.rst'),
    author='Mozilla Foundation',
    author_email='dev-webdev@lists.mozilla.org',
    url='https://github.com/mozilla/redash-stmo',
    license='MPL 2.0',
    entry_points={
        'redash.extensions': [
            'dockerflow = redash_stmo.dockerflow:extension',
            'datasource_health = redash_stmo.data_sources.health:extension',
            'datasource_link = redash_stmo.data_sources.link:extension',
            'datasource_version = redash_stmo.data_sources.version:extension',
            'handler_queryresults = redash_stmo.handlers.query_results:extension',
            'queryrunner_presto = redash_stmo.query_runner.presto:extension',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment :: Mozilla',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
)
