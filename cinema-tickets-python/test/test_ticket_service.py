from ticket_service import TicketService
from ticket_type_request import TicketTypeRequest
from purchase_exceptions import InvalidPurchaseException
from paymentgateway.ticket_payment_service import TicketPaymentService
from seatbooking.seat_reservation_service import SeatReservationService
from unittest.mock import MagicMock, create_autospec
import pytest


#Test Input Validation
def test_ticket_type_requests_fails_for_wrong_type():
    service = TicketService(SeatReservationService(), TicketPaymentService())
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20 , [TicketTypeRequest("ADULT", 3), "String, not a TicketTypeRequest"])

def test_ticket_type_requests_fails_if_adult_absent():
    service = TicketService(SeatReservationService(), TicketPaymentService())
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20, [TicketTypeRequest("CHILD", 3)])

def test_ticket_type_requests_fails_if_number_of_tickets_greater_than_twenty():
    service = TicketService(SeatReservationService(), TicketPaymentService())
    with pytest.raises(InvalidPurchaseException):
        service.purchase_tickets(20, [TicketTypeRequest("ADULT", 200)])

# Test Correct Total Value Is Requested
def test_purchase_amount():
    account_id = 242184218
    seat_reservation_service = create_autospec(SeatReservationService)
    ticket_payment_service = create_autospec(TicketPaymentService)
    service = TicketService(seat_reservation_service, ticket_payment_service)
    service.purchase_tickets(account_id, [TicketTypeRequest("ADULT", 2), TicketTypeRequest("CHILD", 1), TicketTypeRequest("INFANT", 1)])
    ticket_payment_service.make_payment.assert_called_with(account_id = account_id, total_amount_to_pay = 50)

# Test Correct Number of Seats are Requested
def test_number_of_seats():
    account_id = 242184218
    seat_reservation_service = create_autospec(SeatReservationService)
    ticket_payment_service = create_autospec(TicketPaymentService)
    service = TicketService(seat_reservation_service, ticket_payment_service)
    service.purchase_tickets(account_id, [TicketTypeRequest("ADULT", 2), TicketTypeRequest("CHILD", 1), TicketTypeRequest("INFANT", 1)])
    seat_reservation_service.reserve_seat.assert_called_with(account_id = account_id, total_seats_to_allocate = 3)