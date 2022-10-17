from ticket_service import TicketService
from ticket_type_request import TicketTypeRequest
from purchase_exceptions import InvalidPurchaseException
import pytest


#Test Input Validation
def test_account_id_fails_for_non_int():
    service = TicketService()
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets("Not an Integer" , [TicketTypeRequest("ADULT", 3)])

def test_ticket_type_requests_fails_for_wrong_type():
    service = TicketService()
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20 , [TicketTypeRequest("ADULT", 3), "String, not a TicketTypeRequest"])

def test_ticket_type_requests_fails_if_adult_absent():
    service = TicketService()
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20, [TicketTypeRequest("CHILD", 3)])

def test_ticket_type_requests_fails_if_number_of_tickets_greater_than_twenty():
    service = TicketService()
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20, [TicketTypeRequest("ADULT", 200)])