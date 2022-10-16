from ticket_type_request import TicketTypeRequest
import pytest

def test_get_ticket_type():
    ticket_type_request = TicketTypeRequest("ADULT", 3)
    assert(ticket_type_request.get_ticket_type() == "ADULT")

def test_get_ticket_number():
    ticket_type_request = TicketTypeRequest("ADULT", 3)
    assert(ticket_type_request.get_tickets_number() == 3)

def test_incorrect_ticket_type_raises_typeerror():
    with pytest.raises(TypeError):
        TicketTypeRequest("NOTVALIDTYPE", 3)