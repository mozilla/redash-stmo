import os.path

from setuptools import find_packages, setup

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
    use_scm_version={"version_scheme": "post-release", "local_scheme": "dirty-tag"},
    setup_requires=["setuptools_scm"],
    description="Extensions to Redash by Mozilla",
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    entry_points={
        "redash.extensions": [
            "datasource_health = redash_stmo.data_sources.health:extension",
            "datasource_details = redash_stmo.data_sources.details.extension:extension",
            "dockerflow = redash_stmo.dockerflow:extension",
            "handler_queryresults = redash_stmo.handlers.query_results.extension:extension",
            "handler_remote_user_auth = redash_stmo.handlers.authentication.remote_user_auth:extension",
            "queryrunner_big_query = redash_stmo.query_runner.big_query:extension",
            "queryrunner_presto = redash_stmo.query_runner.presto:extension",
        ],
        "redash.bundles": [
            "datasource_details = redash_stmo.data_sources.details",
        ],
        "redash.scheduled_jobs": [
            "update_health_status = redash_stmo.data_sources.health:scheduled_job"
        ],
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires='>=3.5, <4',
    install_requires=[
        "dockerflow>=2018.4.0",
        "pyhive",
        "requests",
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
