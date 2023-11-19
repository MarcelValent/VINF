import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import NIOFSDirectory
import openpyxl
import pandas as pd

def create_index(index_dir, excel_path):
    lucene.initVM()

    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

    fs_directory = NIOFSDirectory(Paths.get(index_dir))
    writer = IndexWriter(fs_directory, config)

    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        doc = Document()
        doc.add(TextField("HomeTeam", str(row[0]), Field.Store.YES))
        doc.add(TextField("AwayTeam", str(row[1]), Field.Store.YES))
        doc.add(TextField("Date", str(row[2]), Field.Store.YES))
        doc.add(TextField("Time", str(row[3]), Field.Store.YES))

        stadium_value = str(row[4]) if row[4] is not None and not pd.isna(row[4]) else ""
        doc.add(TextField("Stadium", stadium_value, Field.Store.YES))

        doc.add(TextField("GoalsHome", str(row[5]), Field.Store.YES))
        doc.add(TextField("GoalsAway", str(row[6]), Field.Store.YES))
        doc.add(TextField("Goals", str(row[7]), Field.Store.YES))
        doc.add(TextField("Cards", str(row[8]), Field.Store.YES))
        doc.add(TextField("RedCards", str(row[9]), Field.Store.YES))

        writer.addDocument(doc)
        #print(doc)
    writer.commit()
    writer.close()


if __name__ == "__main__":
    index_directory = "./index"
    excel_file_path = "./matches.xlsx"

    create_index(index_directory, excel_file_path)
    print("Indexing is done.")
