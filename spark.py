# Import necessary libraries
import bz2
import re
from pyspark.sql import SparkSession
import pandas as pd

# Create a Spark session
spark = SparkSession.builder \
    .appName("XMLDataLoadExample") \
    .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.14.0") \
    .getOrCreate()

# Path to the Excel file containing player data
excel_file_path = "./players.xlsx"
# Read player data from the Excel file into a Pandas DataFrame
df_players = pd.read_excel(excel_file_path)

# Path to the BZ2-compressed XML file
file_path = "./skwiki-latest-pages-articles.xml.bz2"

# Open the BZ2 file and read its content
with bz2.open(file_path, 'rb') as f:
    xml_content = f.read()

# Extract data from the XML content using regular expressions
data = []
matches = re.finditer(r"nár=([^|]+).*meno=\[\[([^]]+)\]\]", xml_content.decode('utf-8'))
for match in matches:
    data_item = {
        "nár": match.group(1),
        "meno": match.group(2),
    }
    data.append(data_item)
print(data)

# Create a Pandas DataFrame from the extracted XML data
df_xml = pd.DataFrame(data)

# Merge player data and XML data based on the "name" and "meno" columns
pandas_df_combined = pd.merge(df_players, df_xml, left_on="name", right_on="meno", how="left")

# Drop the redundant "meno" column
pandas_df_combined = pandas_df_combined.drop("meno", axis=1)

# Calculate the percentage of blank values in the "nár" column
total_rows = len(pandas_df_combined)
blank_percentage = (pandas_df_combined["nár"].isnull().sum() / total_rows) * 100
print("Blank percentage: ", blank_percentage)

# Save the combined DataFrame to an Excel file
pandas_df_combined.to_excel("./output.xlsx", index=False)

# Stop the Spark session
spark.stop()
