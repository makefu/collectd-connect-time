from setuptools import setup, find_packages



classifiers = []
with open("classifiers.txt") as fd:
    classifiers = fd.readlines()


setup(
    name="collectd-connect-time",
    version="0.2.0",
    description="TCP Connection time plugin for collectd.",
    author="Felix Richter",
    author_email="github@syntax-fehler.de",
    url="http://github.com/makefu/collectd-connect-time",
    license="wtfpl",
    classifiers=classifiers,
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    entry_points = {
        'console_scripts' :
            ['collectd-connect-time=collectd_connect_time.collect:cli'],
    },
    install_requires=[],
)
