import pytest

def test_deploy(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!", 5, 100)
    assert snek.name() == "My new event!"
    assert snek.number_of_tickets() == 5
    assert snek.price() == 100


@pytest.fixture(scope='module', autouse=True)
def snek(accounts, TicketSnek):
    yield accounts[0].deploy(TicketSnek, "My new event!", 5, 100)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_buy_tickets(accounts, snek):
    for i, a in enumerate(accounts[:snek.number_of_tickets()]):
        before_funds = snek.balance()
        snek.buy({'from': a, 'value': snek.price()})
        assert snek.has_ticket(a)
        assert snek.balance() - before_funds == snek.price()

def test_overbuy(accounts, snek):
    test_buy_tickets(accounts, snek)  # Start from end of this test

    with pytest.reverts("dev: All tickets sold!"):
        snek.buy({'from': accounts[snek.number_of_tickets()]})

def test_cannot_buy_two_tickets(accounts, snek):
    snek.buy({'from': accounts[0]})
    with pytest.reverts("dev: You already bought a ticket!"):
        snek.buy({'from': accounts[0]})

def test_withdraw_money(accounts, snek):
    test_buy_tickets(accounts, snek)  # Start from end of this test

    assert snek.balance() == 5 * snek.price()
    snek.withdraw({'from': accounts[5]})
    assert snek.balance() == 0
