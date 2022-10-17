from purchase_exceptions import InvalidPurchaseException
from ticket_type_request import TicketTypeRequest

class TicketService:
    
    def __init__(self, seat_reservation_service, ticket_payment_service, max_number_of_tickets=20, ticket_prices ={"ADULT":20, "CHILD":10, "INFANT":0}):
      self.seat_reservation_service = seat_reservation_service
      self.ticket_payment_service = ticket_payment_service
      self.max_number_of_tickets = max_number_of_tickets
      self.ticket_prices = ticket_prices

    # Validation Helper Functions
    def _validate_ticket_type_requests(self, ticket_type_requests):
      for ticket_type_request in ticket_type_requests:
        if not isinstance(ticket_type_request, TicketTypeRequest):
          raise InvalidPurchaseException("Not a Valid Ticket Type Request")
    
    def _validate_number_of_tickets(self, ticket_type_requests):
      total_number_of_tickets = sum([ticket_type_request.get_tickets_number() for ticket_type_request in ticket_type_requests])
      if total_number_of_tickets > self.max_number_of_tickets:
        raise InvalidPurchaseException(f"You can only purchase {self.max_number_of_tickets} tickets")

    def _verify_that_children_and_infants_are_supervised(self, ticket_type_requests):
      list_of_ticket_types = [ticket_type_request.get_ticket_type() for ticket_type_request in ticket_type_requests]
      if "ADULT" not in list_of_ticket_types:
        raise InvalidPurchaseException("An Adult is Required in the Party")

    # Validation Helper Function, encapsulates the individual helper functions
    def _validate_request(self, account_id, ticket_type_requests):
        self._validate_ticket_type_requests(ticket_type_requests)
        self._validate_number_of_tickets(ticket_type_requests)
        self._verify_that_children_and_infants_are_supervised(ticket_type_requests)
    
    # Helper functions calling the seat reservation and payment services
    # Calculates the number of seats needed and submits this to the seat reservation service
    def _make_seat_reservation(self, account_id, ticket_type_requests):
      total_seats = sum([ticket_type_request.get_tickets_number() for ticket_type_request in ticket_type_requests if ticket_type_request.get_ticket_type() != "INFANT"])
      self.seat_reservation_service.reserve_seat(account_id, total_seats)

    # Calculates the total payment due and submits this to the seat reservation service
    def _make_request_to_payment_service(self, account_id, ticket_type_requests):
      total_price = sum([self.ticket_prices[ticket_type_request.get_ticket_type()]*ticket_type_request.get_tickets_number() for ticket_type_request in ticket_type_requests])
      self.ticket_payment_service.make_payment(account_id, total_price)

    def purchase_tickets(self, account_id=None, ticket_type_requests=[]):
        """
        Validates the input of a request, and then makes requests to seat
        reservation and payment services.

          Parameters:
            account_id (int): A positive integer id number representing the user
            ticket_type_requests (List(ticket_type_request.TicketTypeRequest)) a list of TicketTypeRequests representing a purchase request

          Returns:
            None
        """
        self._validate_request(account_id, ticket_type_requests)
        self._make_seat_reservation(account_id, ticket_type_requests)
        self._make_request_to_payment_service(account_id, ticket_type_requests)