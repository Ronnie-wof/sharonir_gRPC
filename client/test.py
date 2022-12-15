import unittest
from unittest.mock import MagicMock
import get_book_titles as get_titles
import inventory_client
from service.book_details_pb2 import Author
from service.book_details_pb2 import Book
import logging

#hardcoded values for mock testing
values = {"978-0-9940969-0-1": {"title":"Tottenham","author":"Jackson","genre":"MYSTERY","year":"1998"}, 
       "978-0-9940969-0-2": {"title":"Biography of Sharoni","author":"Ronnie","genre":"COMEDY","year":"2020" }}

def side_effect(arg):
        response = values[arg]
        author = Author(author = response["author"])
        book = Book(ISBN=arg, title=response["title"], author= author, genre= response["genre"], year = int(response["year"]))
        return book


#Class containing test cases for testing the getBookTitle functionality
class TestClient(unittest.TestCase):
    # #testing using mock
    def test_get_book_title(self):
        mockClient = MagicMock()
        mockClient.getBook.side_effect = side_effect
        list = ["978-0-9940969-0-1","978-0-9940969-0-2"]
        response = get_titles.getTitles(list=list, client=mockClient)
        result = ["Tottenham","Biography of Sharoni"]
        self.assertEqual(response, result)
        print("Testing using mock has run successfully")
    
    #testing without mock. Using live server.
    def test_get_book_title_live(self):
        client = inventory_client.Client("localhost:50051")
        isbns=["978-0-9940969-0-6","978-0-9940969-0-7"]
        list = get_titles.getTitles(list=isbns, client=client)
        expectedResult = ["Nemesis","Tottenham Hill"]
        self.assertEqual(list, expectedResult)
        print("Testing with live server has run successfully")

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
