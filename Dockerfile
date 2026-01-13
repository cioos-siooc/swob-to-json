FROM python:3.14-slim

WORKDIR /app

COPY swob_to_json/ swob_to_json/
COPY test_files/ test_files/
COPY setup.py pyproject.toml README.md ./

RUN pip install --no-cache-dir .

RUN mkdir -p /output_json

CMD for i in /app/test_files/input_xml/*.xml; do \
    echo "Input: $i"; \
    python -m swob_to_json "$i" > "/output_json/$(basename $i).json"; \
    echo "Output: /output_json/$(basename $i).json"; \
    echo; \
done
