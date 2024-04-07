from django.urls import path
from .views import *

urlpatterns = [
    path('books/<int:book_id>/checkout/<int:member_id>', BookCheckoutView.as_view(), name="book_checkout_view"),
    path('books/<int:book_id>/return/<int:member_id>', BookReturnView.as_view(), name="book_return_view"),
    # path('books/<int:book_id>/reserve', BookReserveView.as_view(), name="book_reserve_view"),
    path('books/<int:book_id>/fulfill', BookFulfillView.as_view(), name="book_fulfill_view"),
]