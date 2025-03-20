from distutils.core import setup

setup(
    name="swob_to_json",
    version="1",
    packages=["swob_to_json"],
    install_requires=["click", "xmltodict"],
    license="MIT",
)
