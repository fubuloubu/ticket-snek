# TicketSnek, what does it do?
# 1. Create an event
# 2. Someone can buy a ticket

NUMBER_OF_TICKETS: constant(uint256) = 5

name: public(string[64])
tickets: public(address[NUMBER_OF_TICKETS])


@public
def __init__(_name: string[64]):
    self.name = _name
