from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# Create your views here.

class BookCheckoutView(APIView):
    def post(self, request, **kwargs):
        """
        1. Check out a book when a copy is available in case of a "checkout" request
        3. Reserve a book and move to reservation queue when a particular book has no copies available in case of a "checkout" request.
        """
        try:
            book_id = self.kwargs.get('book_id')
            member_id = self.kwargs.get('member_id')

            # validity check for book_id and member_id
            book = Book.objects.get(BookID=book_id)
            member = Member.objects.get(MemberID=member_id)

            # check if the book_id has available copies
            number_of_copies = book.NumberOfCopies

            if number_of_copies == 0:
                # add the member to the reservation queue
                reservation_queue = Reservation.objects.filter(book=book).order_by('order').values('order')
                # check if the reservation queue exists
                if reservation_queue:
                    # add the member to the queue with incremented order
                    old_order = reservation_queue[-1]['order']
                    new_order = old_order + 1
                    Reservation.objects.create(book=book, order=new_order, member=member)
                else:
                    # create the queue for this book with order = 1
                    Reservation.objects.create(book=book, order=1, member=member)

                return Response({"message": "user added to queue for this book"}, status=status.HTTP_200_OK)

            elif number_of_copies > 0:
                book.NumberOfCopies = number_of_copies - 1
                book.save()

            else:
                pass

            return Response({"message": "book checked out successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class BookReturnView(APIView):
    def post(self, request, **kwargs):
        """
        2. Return a book on a "return" request
        """
        try:
            book_id = self.kwargs.get('book_id')
            member_id = self.kwargs.get('member_id')

            # validity check for book_id and member_id
            book = Book.objects.get(BookID=book_id)
            member = Member.objects.get(MemberID=member_id)

            # increment the number of copies by one
            book.NumberOfCopies = book.NumberOfCopies + 1
            book.save()

            return Response({"message": "book returned successfully"}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class BookFulfillView(APIView):
    def post(self, request, **kwargs):
        """
        4. fulfill/process the reservation queue for a particular book_id
        """
        try:
            book_id = self.kwargs.get('book_id')

            # validity check for book_id and member_id
            book = Book.objects.get(BookID=book_id)

            # check the number of available copies for the book
            available_copies = book.NumberOfCopies

            if available_copies > 0:
                # check if there are elements in the queue for the book
                reservation_queue = Reservation.objects.filter(book=book).order_by('order').values()
                if reservation_queue:
                    # process the queue
                    to_be_deleted_ids = []
                    for el in reservation_queue:
                        to_be_deleted_ids.append(el['id'])
                        available_copies = available_copies - 1
                        if available_copies == 0:
                            break
                    # delete processed ids
                    Reservation.objects.filter(id__in=to_be_deleted_ids).delete()
            else:
                return Response({"message": "book has zero available copies so queue cannot be processed."}, status=status.HTTP_400_BAD_REQUEST)

            book.NumberOfCopies = available_copies
            book.save()
            return Response({"message": "queue processed successfully"}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

