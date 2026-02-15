from seat import Seat

class Ticket:
    def __init__(self, seat: Seat, owner: str):
        self.seat = seat      
        self.owner = owner    