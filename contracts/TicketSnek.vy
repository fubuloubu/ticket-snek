# TicketSnek, what does it do?
# 1. Create an event
# 2. Someone can buy a ticket
# 3. There are a limited number of tickets
# 4. Each ticket has a specific price


name: public(string[64])
tickets: public(map(uint256, address))
number_of_tickets: public(uint256)
last_ticket_sold: uint256

price: public(uint256(wei))


@public
def __init__(_name: string[64], _tickets: uint256, _price: uint256(wei)):
    self.name = _name
    self.number_of_tickets = _tickets
    self.last_ticket_sold = 0
    self.price = _price


@public
@payable
def buy():
    assert self.last_ticket_sold < self.number_of_tickets  # dev: All tickets sold!
    self.tickets[self.last_ticket_sold] = msg.sender
    self.last_ticket_sold += 1
