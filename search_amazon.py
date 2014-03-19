import amazonproduct
#from lxml import etree as ET
#from lxml import objectify

api=amazonproduct.API(cfg=".amazon-product-api", locale="us")

def get_book_by_title_author(title, author):
#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html	
	books = api.item_search("Books", Title=title,
		                             Author=author,
		                             ItemPage=1)

	for book in books:
		book = book.ItemAttributes.Title, book.ItemAttributes.Author, book.DetailPageURL, book.ASIN

		print unicode(book)
		#print "%s: %s, %s, %s" % (book.ItemAttributes.Title,
		#	                      book.ItemAttributes.Author,
		#	                      book.DetailPageURL,
		#	                      book.ASIN)
		#return render_template("amazon_results.html", )
		#print ET.tostring(book, pretty_print=True)		
get_book_by_title_author("The Time Traveler's Wife", "Audrey Niffenegger") 


def get_book_image(asin):
#to get image for specific book by ASIN
#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html#LargeImage	
	book_image = api.item_lookup(ItemId=asin, IDType="ASIN", ResponseGroup="Images")
	image = book_image.Items.Item.ImageSets.ImageSet.LargeImage.URL
	print image
get_book_image("015602943X")


def get_book_description(asin):
#to get description from editorial review 
#can't just get description - may be copyrighted per research
	editorial_review = api.item_lookup(ItemId=asin, IDType="ASIN", ResponseGroup="EditorialReview")
	book_description = editorial_review.Items.Item.EditorialReviews.EditorialReview.Content
	print book_description
get_book_description("015602943X")		