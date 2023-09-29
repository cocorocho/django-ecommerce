from rest_framework.pagination import PageNumberPagination


class StorePaginator(PageNumberPagination):
    page_size = 20
