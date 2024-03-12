from rest_framework.pagination import PageNumberPagination

# ... 
class FeedbackPaginator(PageNumberPagination):
    
    page_query_param = 'p'
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10