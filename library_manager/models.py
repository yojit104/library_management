from django.db import models

# Create your models here.
class Book(models.Model):
    BookID = models.IntegerField(primary_key=True, db_index=True)
    BookName = models.CharField(max_length=500)
    NumberOfCopies = models.IntegerField()

class Member(models.Model):
    MemberID = models.IntegerField(primary_key=True, db_index=True)
    MemberName = models.CharField(max_length=500)

class Reservation(models.Model):
    """
    implementation of a queue to fulfill reservations
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_index=True)
    order = models.IntegerField() # for storing the priority of a user for a particular book
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [models.UniqueConstraint(fields=['book', 'order', 'member'], name="unique_book_id_and_order")] # for a particular book, order is 

# class Circulation(models.Model):

