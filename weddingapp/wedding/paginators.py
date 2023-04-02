from rest_framework import pagination


class MonAnPaginator(pagination.PageNumberPagination):
    page_size = 20


class SanhCuoiPaginator(pagination.PageNumberPagination):
    page_size = 8