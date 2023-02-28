FROM python:3.10

COPY . .

RUN pip install .
RUN for i in test_files/input_xml/*;do python -m swob_xml_to_json $i;done