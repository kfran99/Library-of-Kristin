import amazonproduct
from lxml import etree as ET

api=amazonproduct.API(cfg=".amazon-product-api", locale="us")

def get_book_by_title_author(title, author):
	books = api.item_search("Books", Title=title, 
									Author=author, 
									ItemPage=1)
	#title = books.ItemAttributes.Title
	#author = books.ItemAttributes.Author
	for book in books:
		print "%s: %s" % (book.ItemAttributes.Title, book.ItemAttributes.Author)
		#prints out more details - need to figure out how to get what I want
		#look at http://stackoverflow.com/questions/13093091/lxml-or-lxml-html-print-tree-structure
		print ET.tostring(book, pretty_print=True)

		#return (title, author, pages, description, url for Amazon link to book)
#Eventually want this to go to a template so I can pick the best result for my database and then add it.
#return render_template("amazon_results.html", )		

get_book_by_title_author("The Time Traveler's Wife", "Audrey Niffenegger") 