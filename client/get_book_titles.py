#file containing function for taking list of ISBN's, calling GetBookRPC and retriving the corresponding titles in a list
import logging
import inventory_client 

#function will take in list of ISBN's and the client object as the parameters
def getTitles(list, client):
    result = []
    for x in list:
        #fetching book details of the particular ISBN
        response = client.getBook(x)
        #appending book title to resultant list
        result.append(response.title)
    return result
    


if __name__ == '__main__':
    logging.basicConfig()
    #passing the server address and port
    client = inventory_client.Client("localhost:50051")
    isbns=["978-0-9940969-0-6","978-0-9940969-0-7"]
    #calling function for accessing RPC's
    list = getTitles(list=isbns, client=client)
    for title in list:
        print(title)
    