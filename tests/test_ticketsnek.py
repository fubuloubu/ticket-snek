import pytest

def test_deploy(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!", 5, 100)
    assert snek.name() == "My new event!"
    assert snek.number_of_tickets() == 5
    assert snek.price() == 100

def test_buy_tickets(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!", 7, 100)
    for i, a in enumerate(accounts[:7]):
        before_funds = snek.balance()
        snek.buy({'from': a, 'value': snek.price()})
        assert snek.tickets(i) == a
        assert snek.balance() - before_funds == snek.price()

    with pytest.reverts("dev: All tickets sold!"):
        snek.buy({'from': accounts[7]})
