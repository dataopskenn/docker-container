FROM python:3.9

RUN pip install pandas
RUN pip install numpy
RUN pip install SQLAlchemy
RUN pip install pyarrow
RUN pip install requests

WORKDIR /app

COPY pipeline.py pipeline.py
COPY ingest.py ingest.py
COPY local_ingest.py local_ingest.py

ENTRYPOINT [ "bash" ]