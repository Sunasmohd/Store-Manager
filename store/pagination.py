from rest_framework.pagination import PageNumberPagination as BasePage

class PageNumberPagination(BasePage):
    PAGE_SIZE = 10