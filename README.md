# Books Catalog
This is a python and flask website repository for Book Catalog.
It has the following features:
1. The user can login through facebook and google sign in.
2. Once the user is logged in, they can view the list of book categories and the top 10 recently added books
3. The user can click on any of the category to view all the books in that category.
4. The user has an option to create a new category or add a new book.
5. The user can view the details of a book by clicking on a specific book.
6. When the user is in the book details section, he /she can edit or delete the book if they are the creator of that specific    book.If they have not created that book then then can just view the book details.
7. The user can logout of the website and can view the categories/book. If a user is not logged in he/she will not have the      rights to create/update/delete a book or a category.


## Getting Started

Download the code with git clone https://github.com/mani11/BooksCatalog.git

### Prerequisites

**You should have python3 installed.** 

_Download link_:https://www.python.org/downloads/

**You need VirtualBox tool to run VM.**

_Download Link_: https://www.virtualbox.org/wiki/Download_Old_Builds_5_2

**You need vagrant to configure the VM**

_Download Link_:https://www.vagrantup.com/downloads.html

Once you have the VMBox and vagrant you need to download the configuration for the VM

_Git link_: https://github.com/udacity/fullstack-nanodegree-vm

After the download,you will have a directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

**Start Virtual Machine:**

From your terminal, inside the vagrant subdirectory, run the command _**vagrant up_**. This will cause Vagrant to download the Linux operating system and install it.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run _**vagrant ssh**_ to log in to your newly installed Linux VM!

**Running the database**

This project uses sqlite3 database.
Inside the vagrant folder run the database_setup.py file to create the database tables.
Run the command _**python database_setup.py**_


**Populate data**

Next, populate the database with some dummy data created in the dataset.py file
Run the command _**python dataset.py**_

**Run the website**

Next, run the application with _**python Books.py**_ command. This will start the server at port 5000.
Now from the browser visit _**localhost:5000/login**_ to land on the login page. To visit the home page visit _**localhost:5000/catalog**_
or _**localhost:5000/**_

**API end point**
To view the data in the json format visit 
1. API end point /Catalog/JSON to get the json endpoint for the Books Catalog data
2. API end point /Category/JSON to get all book categories
3. API end point /Category/<int:id>/Books/JSON to get all books for a specified category
4. API end point /Category/<int:category_id>/Books/<int:book_id>/JSON to get a specified book












