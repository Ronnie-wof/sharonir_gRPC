from concurrent import futures
import logging
import grpc
import book_details_pb2_grpc as book_details_pb2_grpc
from book_details_pb2 import Genre
from book_details_pb2 import Book
from book_details_pb2 import Author
from book_details_pb2 import createBookOutput

#hardcoded dictionary of books used for testing out the server
books = {
        "978-0-9940969-0-6": {"title":"Nemesis","author":"Bill","genre":"MYSTERY","year":"2016"},
        "978-0-9940969-0-7": {"title":"Tottenham Hill","author":"Shakira","genre":"ROMANCE","year":"2016"},
        "978-0-9940969-0-8": {"title":"Jacksonville","author":"Sharoni","genre":"MYSTERY","year":"2020"},
    }

genres = [
    "THRILLER", "MYSTERY", "COMEDY", "HORROR", "ROMANCE"
]
#class containing the implementation of the RPC's
class Inventory(book_details_pb2_grpc.InventoryServiceServicer):
    # CreateBook RPC implementation
    def CreateBook(self, request, context):
        #if given genre is not part of the enum list
        if request.genre not in Genre.values():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Genre provided is not an acceptable one. Please enter from this list[THRILLER, MYSTERY, COMEDY, HORROR, ROMANCE]")
            return createBookOutput(response ="Invalid input.Cannot create book.")
        #adding to dictionary
        books[request.ISBN] = request
        return createBookOutput(response ="Successfully created!")

    # GetBook RPC implementation
    def GetBook(self, request, context):
        #if isbn provided does not exist in our storage
        if request.isbn not in books.keys():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("ISBN of book provided does not exist in our system.")
            return Book()
        #fetching book from storage
        x=books.get(request.isbn)
        name = x["author"]
        author = Author(author=name)
        book = Book(ISBN=request.isbn, title=x["title"], author= author, genre= x["genre"], year = int(x["year"]))
        return book

#setting up the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_details_pb2_grpc.add_InventoryServiceServicer_to_server(Inventory(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()

    