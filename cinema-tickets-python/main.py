
from ticket_service import TicketService
from ticket_type_request import TicketTypeRequest
from paymentgateway.ticket_payment_service import TicketPaymentService
from seatbooking.seat_reservation_service import SeatReservationService

if __name__ == '__main__':

    ticket_service = TicketService(SeatReservationService(), TicketPaymentService())

    ticket_service.purchase_tickets(242184218, [TicketTypeRequest("ADULT", 2), TicketTypeRequest("CHILD", 1), TicketTypeRequest("INFANT", 1)])
