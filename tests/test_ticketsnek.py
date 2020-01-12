import pytest

EVENT_NAME = "My new event!"
NUMBER_TICKETS = 5
TICKET_PRICE = 100  # wei
FIVE_SECONDS = 5
SNEK_ARGS = [EVENT_NAME, NUMBER_TICKETS, TICKET_PRICE, FIVE_SECONDS]


def test_deploy(rpc, accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, *SNEK_ARGS, rpc.time() + FIVE_SECONDS)
    assert snek.name() == EVENT_NAME
    assert snek.number_of_tickets() == NUMBER_TICKETS
    assert snek.price() == TICKET_PRICE


@pytest.fixture(scope='module', autouse=True)
def snek(rpc, accounts, TicketSnek):
    yield accounts[0].deploy(TicketSnek, *SNEK_ARGS, rpc.time() + FIVE_SECONDS)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_buy_tickets(accounts, snek):
    for i, a in enumerate(accounts[:snek.number_of_tickets()]):
        before_funds = snek.balance()
        snek.buy({'from': a, 'value': snek.price()})
        assert snek.has_ticket(a)
        assert snek.balance() - before_funds == snek.price()

def test_must_send_right_price(accounts, snek):
    with pytest.reverts("dev: Must send exactly the price of a ticket!"):
        snek.buy({'from': accounts[0], 'value': snek.price()+1})

def test_overbuy(accounts, snek):
    test_buy_tickets(accounts, snek)  # Start from end of this test

    with pytest.reverts("dev: All tickets sold!"):
        snek.buy({'from': accounts[snek.number_of_tickets()], 'value': snek.price()})

def test_cannot_buy_two_tickets(accounts, snek):
    snek.buy({'from': accounts[0], 'value': snek.price()})
    with pytest.reverts("dev: You already bought a ticket!"):
        snek.buy({'from': accounts[0], 'value': snek.price()})

def test_cant_buy_after_event_starts(rpc, accounts, snek):
    rpc.sleep(FIVE_SECONDS)

    with pytest.reverts("dev: Cannot buy tickets after the event started!"):
        snek.buy({'from': accounts[0], 'value': snek.price()})


def test_can_get_refund(accounts, snek):
    snek.buy({'from': accounts[0], 'value': snek.price()})

    with pytest.reverts("dev: You don't have a ticket!"):
        snek.refund({'from': accounts[1]})

    assert snek.tickets_sold() == 1
    snek.refund({'from': accounts[0]})
    assert snek.tickets_sold() == 0

def test_cant_refund_after_period_ends(rpc, accounts, snek):
    snek.buy({'from': accounts[0], 'value': snek.price()})

    rpc.sleep(FIVE_SECONDS)

    with pytest.reverts("dev: Refund window has closed!"):
        snek.refund({'from': accounts[0]})

def test_withdraw_money(rpc, accounts, snek):
    test_buy_tickets(accounts, snek)  # Start from end of this test

    with pytest.reverts("dev: Must be Snek Charmer!"):
        snek.withdraw({'from': accounts[NUMBER_TICKETS]})

    with pytest.reverts("dev: Event hasn't settled yet!"):
        snek.withdraw({'from': accounts[0]})

    rpc.sleep(FIVE_SECONDS + 7 * 24 * 60 * 60)

    assert snek.balance() == NUMBER_TICKETS * snek.price()
    snek.withdraw({'from': accounts[0]})
    assert snek.balance() == 0
