from distutils.core import setup

setup(
    name="swob_xml_to_json",
    version="0.1",
    packages=['swob_xml_to_json'],
    install_requires=["click", "xmltodict"],
    license="MIT",
)
