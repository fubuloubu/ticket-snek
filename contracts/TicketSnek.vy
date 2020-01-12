# TicketSnek, what does it do?
# 1. The Admin creates an event
# 2. Someone can buy a ticket
# 3. There are a limited number of tickets
# 4. Each ticket has a specific price
# 5. A user can only buy one ticket
# 6. A user can get a refund by giving their ticket back before the refund period ends
# 7. The Admin can withdraw proceeds of the event 7 weeks after it starts

# This ensures that there is enough time after the event has completed
# to process disputes about the event
SETTLEMENT_TIME: constant(timedelta) = 7 * 24 * 60 * 60  # 7 days


name: public(string[64])
event_date: public(timestamp)
snek_charmer: public(address)
has_ticket: public(map(address, bool))
number_of_tickets: public(uint256)
tickets_sold: public(uint256)

price: public(uint256(wei))
refund_window_ends: timestamp


@public
def __init__(
    _name: string[64],
    _tickets: uint256,
    _price: uint256(wei),
    _refund_window: timedelta,
    _event_date: timestamp,
):
    self.name = _name
    self.event_date = _event_date
    self.snek_charmer = msg.sender
    self.number_of_tickets = _tickets
    self.tickets_sold = 0
    self.price = _price
    self.refund_window_ends = block.timestamp + _refund_window
    assert self.refund_window_ends <= self.event_date  # dev: Refund window must end before event starts!


@public
@payable
def buy():
    assert block.timestamp < self.event_date  # dev: Cannot buy tickets after the event started!
    assert msg.value == self.price  # dev: Must send exactly the price of a ticket!
    assert self.tickets_sold < self.number_of_tickets  # dev: All tickets sold!
    assert not self.has_ticket[msg.sender]  # dev: You already bought a ticket!
    self.has_ticket[msg.sender] = True
    self.tickets_sold += 1


@public
def refund():
    assert self.has_ticket[msg.sender]  # dev: You don't have a ticket!
    assert self.refund_window_ends > block.timestamp  # dev: Refund window has closed!
    self.has_ticket[msg.sender] = False  # Re-entrancy protection
    self.tickets_sold -= 1
    send(msg.sender, self.price)


@public
def withdraw():
    assert msg.sender == self.snek_charmer  # dev: Must be Snek Charmer!
    assert self.event_date + SETTLEMENT_TIME < block.timestamp  # dev: Event hasn't settled yet!
    selfdestruct(msg.sender)
