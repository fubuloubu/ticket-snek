import pytest

def test_deploy(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!", 5)
    assert snek.name() == "My new event!"
    assert snek.number_of_tickets() == 5

def test_buy_tickets(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!", 7)
    for i, a in enumerate(accounts[:7]):
        snek.buy({'from': a})
        assert snek.tickets(i) == a

    with pytest.reverts("Index out of range"):
        snek.buy({'from': accounts[7]})
