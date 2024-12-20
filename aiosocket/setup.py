from setuptools import find_packages, setup

setup(
    name="aiosocket",
    packages=find_packages(include=["aiosocket", "aiosocket.*"]),
    version="0.1.0",
    description="Asyncio socket library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/retract1337/aiosocket",
    author="i@retracted.in",
)
