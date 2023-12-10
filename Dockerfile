FROM coady/pylucene
WORKDIR /usr/src/app
RUN pip install pandas
RUN pip install pyspark
RUN pip install openpyxl
COPY . .
CMD ["python3", "-m", "http.server", "80"]