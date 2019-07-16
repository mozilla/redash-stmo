from setuptools import setup, find_packages
import os.path

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.rst")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")


setup(
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="redash-stmo",
    version="2019.7.3",
    description="Extensions to Redash by Mozilla",
    python_requires="==2.*,>=2.7.0",
    project_urls={"homepage": "https://github.com/mozilla/redash-stmo"},
    author="Mozilla Foundation",
    author_email="dev-webdev@lists.mozilla.org",
    license="MPL-2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment :: Mozilla",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
    entry_points={
        "redash.extensions": [
            "datasource_health = redash_stmo.data_sources.health:extension",
            "datasource_link = redash_stmo.data_sources.link.extension:extension",
            "datasource_validator = redash_stmo.data_sources.validator.extension:extension",
            "datasource_version = redash_stmo.data_sources.version.extension:extension",
            "dockerflow = redash_stmo.dockerflow:extension",
            "handler_queryresults = redash_stmo.handlers.query_results.extension:extension",
            "handler_remote_user_auth = redash_stmo.handlers.authentication.remote_user_auth:extension",
            "queryrunner_presto = redash_stmo.query_runner.presto:extension",
            "integrations_iodide = redash_stmo.integrations.iodide.extension:extension",
        ],
        "redash.bundles": [
            "datasource_link = redash_stmo.data_sources.link",
            "datasource_version = redash_stmo.data_sources.version",
            "integrations_iodide = redash_stmo.integrations.iodide",
        ],
        "redash.periodic_tasks": [
            "update_health_status = redash_stmo.data_sources.health:periodic_task"
        ],
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "dockerflow>=2018.4.0",
        "pgsanity",
        "pyhive",
        "requests",
        "six",
        "sqlparse",
    ],
    extras_require={
        "test": [
            "flake8==3.5.0",
            "mock",
            "pytest",
            "pytest-cov",
            "pytest-flake8<1.0.1",
        ],
        "dev": ["watchdog"],
    },
)
