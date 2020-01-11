# TicketSnek, what does it do?
# 1. Create an event
# 2. Someone can buy a ticket


name: public(string[64])
tickets: public(map(uint256, address))
number_of_tickets: public(uint256)
last_ticket_sold: uint256


@public
def __init__(_name: string[64], _tickets: uint256):
    self.name = _name
    self.number_of_tickets = _tickets
    self.last_ticket_sold = 0


@public
def buy():
    self.tickets[self.last_ticket_sold] = msg.sender
    self.last_ticket_sold += 1
