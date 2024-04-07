*Database Design*

We have created three models: Book, Member and Reservation.
Book and Member store the book and member data given to us.
Reservation stores the queue for a particular book. The position of a member for a particular queue is determined by the 'order' parameter.

*API Design*

We have three methods: checkout, return and fulfill.
All three methods are called on the bookID. 
Checkout reduces the available count of the book by one. If the available count is zero, its adds the member to the reservation queue.
Return increments the available count of the book by one.
Fulfill processes the queue till the available count is zero or the queue becomes empty for a particular book

*Optimizations*

Indexes have been created for bookID in Book model, memberID in Member model and book foreign key in Reservation model since they have the highest cardinality
