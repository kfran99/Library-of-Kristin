import amazonproduct

api=amazonproduct.API(cfg=".amazon-product-api", locale="us")

def get_book_by_title(title):
	items = api.item_search("Books", Title=title, ItemPage=1)
	for item in items:
		print unicode(item.ItemAttributes.Title)

get_book_by_title("Little Women") 

