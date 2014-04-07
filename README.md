Library-of-Kristin
==================

Hackbright Project

I've always loved reading and my friends and family are constantly borrowing books or asking me for book recommendations.
I love sharing books that I've read, but I often can't remember all the books I have on my books shelves and sometimes I
forget who has borrowed books from me.  I created the Library of Kristin as a way to share my love of reading with friends
and family.

The Library of Kristin is a basic web app, written using Python, Jinja, Flask, HTML, and CSS.  As the administrator of it, I can log in and add books to my database by using the Amazon API.  I type in the title and author of the book and it then pulls all the books from Amazon matching the title and author.  I can see the title, author, ASIN, and the link to the Amazon URL for that book.  If I click on "add book", the ASIN (Amazon Standard Identification Number) is used to all get an image of the book, the description of the book, and the genre of the book.  This is then all added to my database.

Other users can set up an account and then search for books by title and/or author.  The search terms do not need to be
exact.  I set it up to search using SQLAlchemy and used the "ilike" method to search the database.  If no books match
the search terms use, the user is flashed a message saying that no books were found matching the search 
is given, all books in my database are displayed.  Once a user has found a book he/she is interested in borrowing, the user can click on a link to borrow a book.  The user will then see a message saying "You have requested to borrow this 
book." I linked up Twilio to the request link.  When a user requests a book, I get a message on my phone telling me who requested which book.  The history of how many times the book has been checked out is recorded in my database.  It's set up so that as the administrator, I can check the book back in once it is returned to me.

I hope to deploy my web app soon so that my friends can actually use it!
