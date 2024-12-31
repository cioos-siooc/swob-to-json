FROM python:3.10-slim
COPY swob_to_json swob_to_json/
COPY test_files test_files/
COPY setup.py .

RUN pip install .
RUN mkdir -p /output_json

CMD for i in /test_files/input_xml/*.xml; do echo Input: $i; python -m swob_to_json $i > /output_json/$(basename $i).json;echo Output: /output_json/$(basename $i).json; echo ; done
