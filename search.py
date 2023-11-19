import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser

def search_index(index_dir, query_str):

    fs_directory = NIOFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(fs_directory)
    searcher = IndexSearcher(reader)

    fields = ["HomeTeam", "AwayTeam", "Date", "Time", "Stadium", "GoalsHome", "GoalsAway", "Goals", "Cards", "RedCards"]
    analyzer = StandardAnalyzer()
    parser = MultiFieldQueryParser(fields,analyzer)
    queries = parser.parse(parser,query_str)

    hits = searcher.search(queries, 10)

    print(f"Found {hits.totalHits} document(s) that matched the query '{query_str}':")

    #for hit in hits.scoreDocs:
        #doc = searcher.doc(hit.doc)
        #print(f"Document: HomeTeam={doc.get('HomeTeam')}, AwayTeam={doc.get('AwayTeam')}, Date={doc.get('Date')}, Time={doc.get('Time')}, Stadium={doc.get('Stadium')}, GoalsHome={doc.get('GoalsHome')}, GoalsAway={doc.get('GoalsAway')}, Goals={doc.get('Goals')}, Cards={doc.get('Cards')}, RedCards={doc.get('RedCards')}")

    reader.close()


if __name__ == "__main__":
    lucene.initVM()
    index_directory = "./index"  # Change this to the path where you indexed the data
    while True:
        query_string = input("Your search query here: ")  # Modify this with your specific search query
        search_index(index_directory, query_string)