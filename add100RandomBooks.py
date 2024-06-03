#!/usr/bin/env python3

import requests
import json
from faker import Faker


APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

def getAllBooks(apiKey):
    r = requests.get(
        f"{APIHOST}/api/v1/books",
        headers={"X-API-Key": apiKey}
    )
    books = []
    if r.status_code == 200:
        books = r.json()
        print("All Books:")
        for book in books:
            print(book)
            books.append(book)
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to get all books.")
    return books

def deleteBook(id, apiKey):
    r = requests.delete(
            f"{APIHOST}/api/v1/books",
            headers = {
                "X-API-KEY": apiKey}
            )
    if r.status_code == 200:
        print(f"Book {id} has been deleted")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to delete book {id}.")

# Get the Auth Token Key
apiKey = getAuthToken()

# Using the faker module, generate random "fake" books
fake = Faker()
for i in range(25):
    fakeTitle = fake.catch_phrase()
    fakeAuthor = fake.name()
    fakeISBN = fake.isbn13()
    book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
    # add the new random "fake" book using the API
    addBook(book, apiKey)

allBooks = getAllBooks(apiKey)
count = len(allBooks)
if count > 5:
    for i in range(5):
        deleteBook(allBooks[i].id, apiKey)
    for i in range(count-5, count):
        deleteBook(allBooks[i].id, apiKey)
