import amazonproduct
from lxml import etree as ET
from lxml import objectify

api=amazonproduct.API(cfg=".amazon-product-api", locale="us")

def get_book_by_title_author(title, author):
#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html	
	books = api.item_search("Books", Title=title, 
		                             Author=author)
	return books
	#this is going to happen in my controller and iterate through Jinja
	for book in books:
		title = book.ItemAttributes.Title
		author = book.ItemAttributes.Author
		link_to_amazon = book.DetailPageURL
		asin = book.ASIN
		#book = book.ItemAttributes.Title, book.ItemAttributes.Author, book.DetailPageURL, book.ASIN
		print unicode(title), unicode(author), unicode(link_to_amazon), unicode(asin)		
		#return render_template("amazon_results.html", )
		#print ET.tostring(book, pretty_print=True)		
get_book_by_title_author("The Historian", "Elizabeth Kostova") 


def get_book_info(asin):
	#to get image for specific book by ASIN
	#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html#LargeImage	
	book_image = api.item_lookup(ItemId=asin, 
		                         IdType="ASIN", 
		                         ResponseGroup="Images")
	image = book_image.Items.Item.ImageSets.ImageSet.LargeImage.URL
	print image
	#to get description from editorial review
	#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/RG_EditorialReview.html 
	editorial_review = api.item_lookup(ItemId=asin, 
		                               IdType="ASIN", 
		                               ResponseGroup="EditorialReview")
	book_description = editorial_review.Items.Item.EditorialReviews.EditorialReview.Content
	print unicode(book_description)
	#For more info - http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html	
	book_genre = api.item_lookup(ItemId=asin, 
		                         IdType="ASIN",
		                         ResponseGroup="BrowseNodes")
	genre = book_genre.Items.Item.BrowseNodes.BrowseNode.Name
	print genre
get_book_info("0316070637")


