from paymentgateway.ticket_payment_service import TicketPaymentService
from purchase_exceptions import InvalidPurchaseException
from ticket_type_request import TicketTypeRequest
from seatbooking.seat_reservation_service import SeatReservationService

class TicketService:

    _MAX_NUMBER_OF_TICKETS=20
    _TICKET_PRICES = {"ADULT":20, "CHILD":10, "INFANT":0}

    def __init__(self, seat_reservation_service, ticket_payment_service):
      self.seat_reservation_service = seat_reservation_service
      self.ticket_payment_service = ticket_payment_service

    def _validate_account_id(self, account_id):
      if not isinstance(account_id, int):
        raise InvalidPurchaseException("Not an Integer")

    def _validate_ticket_type_requests(self, ticket_type_requests):
      for ticket_type_request in ticket_type_requests:
        if not isinstance(ticket_type_request, TicketTypeRequest):
          raise InvalidPurchaseException("Not a Valid Ticket Type Request")
    
    def _validate_number_of_tickets(self, ticket_type_requests):
      total_number_of_tickets = sum([ticket_type_request.number_of_tickets for ticket_type_request in ticket_type_requests])
      if total_number_of_tickets > self._MAX_NUMBER_OF_TICKETS:
        raise InvalidPurchaseException("You can only purchase 20 tickets")

    def _verify_that_children_and_infants_are_supervised(self, ticket_type_requests):
      list_of_ticket_types = [ticket_type_request.ticket_type for ticket_type_request in ticket_type_requests]
      if "ADULT" not in list_of_ticket_types:
        raise InvalidPurchaseException("An Adult is Required in the Party")

    def _validate_request(self, account_id, ticket_type_requests):
        self._validate_ticket_type_requests(ticket_type_requests)
        self._validate_account_id(account_id)
        self._validate_number_of_tickets(ticket_type_requests)
        self._verify_that_children_and_infants_are_supervised(ticket_type_requests)
    
    def _make_seat_reservation(self, account_id, ticket_type_requests):
      total_seats = sum([ticket_type_request.number_of_tickets for ticket_type_request in ticket_type_requests if ticket_type_request.get_ticket_type() != "INFANT"])
      self.seat_reservation_service.reserve_seat(account_id, total_seats)
      print(total_seats)

    def _make_request_to_payment_service(self, account_id, ticket_type_requests):
      total_price = sum([self._TICKET_PRICES[ticket_type_request.get_ticket_type()]*ticket_type_request.number_of_tickets for ticket_type_request in ticket_type_requests])
      self.ticket_payment_service.make_payment(account_id, total_price)
      print(total_price)

    def purchase_tickets(self, account_id=None, ticket_type_requests=[]):
        self._validate_request(account_id, ticket_type_requests)
        self._make_seat_reservation(account_id, ticket_type_requests)
        self._make_request_to_payment_service(account_id, ticket_type_requests)


# # debugging code
service = TicketService(SeatReservationService(), TicketPaymentService())
service.purchase_tickets(20, [TicketTypeRequest("ADULT",3), TicketTypeRequest("CHILD", 2), TicketTypeRequest("INFANT", 3)])