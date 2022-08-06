FROM python:3.9

RUN pip install pandas
RUN pip install numpy
RUN pip install SQLAlchemy
RUN pip install pyarrow

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "bash" ]