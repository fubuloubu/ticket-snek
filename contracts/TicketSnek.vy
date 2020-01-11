# TicketSnek, what does it do?
# 1. Create an event
# 2. Someone can buy a ticket

NUMBER_OF_TICKETS: constant(uint256) = 7

name: public(string[64])
tickets: public(address[NUMBER_OF_TICKETS])
last_ticket_sold: uint256


@public
def __init__(_name: string[64]):
    self.name = _name
    self.last_ticket_sold = 0


@public
def buy():
    self.tickets[self.last_ticket_sold] = msg.sender
    self.last_ticket_sold += 1
