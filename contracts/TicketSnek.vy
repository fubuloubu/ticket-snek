# TicketSnek, what does it do?
# 1. Create an event
# 2. Someone can buy a ticket
# 3. There are a limited number of tickets
# 4. Each ticket has a specific price
# 5. A user can only buy one ticket



name: public(string[64])
has_ticket: public(map(address, bool))
number_of_tickets: public(uint256)
tickets_sold: public(uint256)

price: public(uint256(wei))


@public
def __init__(_name: string[64], _tickets: uint256, _price: uint256(wei)):
    self.name = _name
    self.number_of_tickets = _tickets
    self.tickets_sold = 0
    self.price = _price


@public
@payable
def buy():
    assert self.tickets_sold < self.number_of_tickets  # dev: All tickets sold!
    assert not self.has_ticket[msg.sender]  # dev: You already bought a ticket!
    self.has_ticket[msg.sender] = True
    self.tickets_sold += 1


@public
def withdraw():
    selfdestruct(msg.sender)
