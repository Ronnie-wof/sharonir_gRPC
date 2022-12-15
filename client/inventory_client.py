#gRPC Client for our API
from __future__ import print_function
from os.path import dirname, realpath
import sys
# For relative imports to work in Python 3.6
sys.path.append(dirname(dirname(realpath(__file__))))

import logging
import grpc
import service.book_details_pb2_grpc as book_details_pb2_grpc
import service.book_details_pb2 as book_details_pb2

class Client:

    def __init__(self, p):
        self.port=p

    #calls the server for accessing createBook RPC
    def createBook(self, book):
        with grpc.insecure_channel(self.port) as channel:
            stub = book_details_pb2_grpc.InventoryServiceStub(channel)
            createBookResponse = stub.CreateBook(book)
            return createBookResponse

    #calls the server for accessing GETBook RPC
    def getBook(self, isbn):
         with grpc.insecure_channel(self.port) as channel:
            stub = book_details_pb2_grpc.InventoryServiceStub(channel)
            getBookInput = book_details_pb2.getBookInput(isbn=isbn) 
            getBookresponse = stub.GetBook(getBookInput)
            return getBookresponse


    