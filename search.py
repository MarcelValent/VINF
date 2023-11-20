import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser


def display_menu():
    print("Choose an option:")
    print("1. Goals")
    print("2. Red Cards")
    print("3. Yellow Cards")


def get_query_field(option):
    fields = {
        "1": ["Goals"],
        "2": ["RedCards"],
        "3": ["YellowCards"]
        # Add more options if needed
    }
    return fields.get(option, [])


def search_index(index_dir, query_str, query_fields):
    fs_directory = NIOFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(fs_directory)
    searcher = IndexSearcher(reader)

    analyzer = StandardAnalyzer()

    parser = MultiFieldQueryParser(query_fields, analyzer)
    queries = parser.parse(parser,query_str)

    hits = searcher.search(queries, 10)

    print(f"Player '{query_str}' has {hits.totalHits} for {query_fields}")

    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        print(f"Document: {', '.join([f'{field}={doc.get(field)}' for field in query_fields])}")
    print("\n\n")

    reader.close()


if __name__ == "__main__":
    lucene.initVM()
    index_directory = "./index"

    while True:
        display_menu()
        option = input("Enter your choice (1-3): ")

        if option not in ["1", "2", "3"]:
            print("Invalid option. Please choose a valid option.")
            continue

        query_fields = get_query_field(option)
        query_string = input("Your keyword to search here: ")

        if query_fields:
            search_index(index_directory, query_string, query_fields)
        else:
            print("Invalid option. Please choose a valid option.")
