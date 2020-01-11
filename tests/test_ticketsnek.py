import pytest

def test_deploy(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!")
    assert snek.name() == "My new event!"

def test_buy_tickets(accounts, TicketSnek):
    snek = accounts[0].deploy(TicketSnek, "My new event!")
    for i, a in enumerate(accounts[:5]):
        snek.buy({'from': a})
        assert snek.tickets(i) == a

    with pytest.reverts("Index out of range"):
        snek.buy({'from': accounts[5]})
