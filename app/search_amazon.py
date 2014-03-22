import amazonproduct
from lxml import etree as ET
from lxml import objectify

api=amazonproduct.API(cfg=".amazon-product-api", locale="us")

def get_book_by_title_author(title, author):
#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
	books = api.item_search("Books", Title=title, 
		                             Author=author,
		                             ItemPage=1)
	return books


def get_book_info(asin):
	print asin , "asin"
	#to get image for specific book by ASIN
	#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html#LargeImage	
	image_url = api.item_lookup(ItemId=asin, 
		                         IdType="ASIN", 
		                         ResponseGroup="Images")

	#to get description from editorial review
	#http://docs.aws.amazon.com/AWSECommerceService/latest/DG/RG_EditorialReview.html 
	editorial_review = api.item_lookup(ItemId=asin, 
		                               IdType="ASIN", 
		                               ResponseGroup="EditorialReview")
	#For more info - http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html	
	book_genre = api.item_lookup(ItemId=asin, 
		                         IdType="ASIN",
		                         ResponseGroup="BrowseNodes")
	print book_genre.Items.Item.BrowseNodes.BrowseNode.Name
	print unicode(editorial_review.Items.Item.EditorialReviews.EditorialReview.Content)
	print image_url.Items.Item.ImageSets.ImageSet.LargeImage.URL
	return image_url, editorial_review, book_genre