import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.queryparser.classic import QueryParser


def display_top_menu():
    print("Choose an option:")
    print("1. Search in Matches")
    print("2. Search in Players")
    print("3. Unit tests")


def display_match_menu():
    print("Choose an option:")
    print("1. Goals")
    print("2. Red Cards")
    print("3. Yellow Cards")


def display_player_menu():
    print("Choose an option:")
    print("1. Goals")
    print("2. Red Cards")
    print("3. Yellow Cards")


def get_query_field(option):
    match_fields = {
        "1": ["Goals"],
        "2": ["RedCards"],
        "3": ["YellowCards"]
    }

    player_fields = {
        "1": ["goals"],
        "2": ["red_cards"],
        "3": ["yellow_cards"]
    }

    return match_fields.get(option, []), player_fields.get(option, [])


def search_index(index_dir, query_str, query_fields):
    fs_directory = NIOFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(fs_directory)
    searcher = IndexSearcher(reader)

    analyzer = StandardAnalyzer()
    parser = MultiFieldQueryParser(query_fields, analyzer)
    queries = parser.parse(parser, query_str)

    hits = searcher.search(queries, 10)

    #print(f"Found {hits.totalHits} document(s) that matched the query '{query_str}':")

    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        print(f"Document: {', '.join([f'{field}={doc.get(field)}' for field in query_fields])}")
        return f"Document: {', '.join([f'{field}={doc.get(field)}' for field in query_fields])}"

    reader.close()


def search_index_players(index_dir, query_str, query_fields):
    fs_directory = NIOFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(fs_directory)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    parser = MultiFieldQueryParser(["name"], analyzer)
    queries = parser.parse(parser, query_str)
    hits = searcher.search(queries, 10)

    #print(f"Found {hits.totalHits} document(s) that matched the query '{query_str}':")

    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        print("Name=", doc.get("name"))
        print(f"{', '.join([f'{field}={doc.get(field)}' for field in query_fields])}")
        return f"{', '.join([f'{field}={doc.get(field)}' for field in query_fields])}"

    reader.close()


if __name__ == "__main__":
    lucene.initVM()
    index_directory = "./index"
    index_directory_players = "./index_players"

    while True:
        display_top_menu()
        top_option = input("Enter your choice (1-3): ")

        if top_option == "1":
            display_match_menu()
            option = input("Enter your choice (1-3): ")
            match_fields, player_fields = get_query_field(option)
            query_string = input("Your keyword to search here: ")
            search_index(index_directory, query_string, match_fields)
        elif top_option == "2":
            display_player_menu()
            option = input("Enter your choice (1-3): ")
            match_fields, player_fields = get_query_field(option)
            query_string = input("Your keyword to search here: ")
            search_index_players(index_directory_players, query_string, player_fields)
        elif top_option == "3":
            inputs = ["Milan Ristovski", "Aleksandar Čavrič", "Matúš Marcin", "Boris Godál", "Boris Godál"]
            expected_outputs = ["goals=28", "goals=45", "yellow_cards=12", "yellow_cards=39", "red_cards=3"]
            options = ["1", "1", "3", "3", "2"]
            zipped = list(zip(inputs, expected_outputs, options))
            for x, y, z in zipped:
                display_player_menu()
                option = z
                match_fields, player_fields = get_query_field(option)
                query_string = x
                result = search_index_players(index_directory_players, query_string, player_fields)
                print("Output:", result)
                print("Expected output: ", y)
                if result == y:
                    print("Result: Successful")
                else:
                    print("Result: Failed")
        else:
            print("Invalid option. Please choose a valid option.")
            continue

