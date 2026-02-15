from seat import Seat
from ticket import Ticket
from cinema_session import CinemaSession 

session = CinemaSession("Avatar 2", 5)
print(session.available_seats())

ticket1 = session.book_seat(3, "Ali")
print(ticket1.owner)          
print(ticket1.seat.number)    
print(ticket1.seat.is_taken)  

print(session.available_seats())

ticket2 = session.book_seat(1, "Vali")

print(session.available_seats())

print(session)

print(f"Jami bron: {len(session.bookings)}")
for ticket in session.bookings:
    print(f"O'rin {ticket.seat.number}: {ticket.owner}")