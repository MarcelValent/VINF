from pyspark import SparkConf
import bz2
import re
from pyspark.sql import SparkSession
import os
import pandas as pd
import pyspark

spark = SparkSession.builder \
    .appName("XMLDataLoadExample") \
    .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.14.0") \
    .getOrCreate()


excel_file_path = "./players.xlsx"
df_players = pd.read_excel(excel_file_path)
file_path = "./skwiki-latest-pages-articles.xml.bz2"

with bz2.open(file_path, 'rb') as f:
    xml_content = f.read()

data = []
matches = re.finditer(r"nár=([^|]+).*meno=\[\[([^]]+)\]\]", xml_content.decode('utf-8'))
for match in matches:
    data_item = {
        "nár": match.group(1),
        "meno": match.group(2),
    }
    data.append(data_item)
print(data)
df_xml = pd.DataFrame(data)
pandas_df_combined = pd.merge(df_players, df_xml, left_on="name", right_on="meno", how="left")
pandas_df_combined = pandas_df_combined.drop("meno", axis=1)
total_rows = len(pandas_df_combined)
blank_percentage = (pandas_df_combined["nár"].isnull().sum() / total_rows) * 100
print("Blank percentage: ", blank_percentage)
pandas_df_combined.to_excel("./output.xlsx", index=False)
spark.stop()
