FROM python:3.10-slim

COPY swob_xml_to_json test_files setup.py .

RUN pip install .
RUN for i in test_files/input_xml/*;do python -m swob_xml_to_json $i > $(dirname $i)/../output_json/$(basename $i).json;done