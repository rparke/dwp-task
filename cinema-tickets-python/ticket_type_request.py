
class TicketTypeRequest(object):

    _valid_types = ("ADULT", "CHILD", "INFANT")

    def __init__(self, ticket_type, number_of_tickets):

        if not isinstance(ticket_type, str):

            raise TypeError("ticket_type must be a string")

        if not ticket_type in self._valid_types:

            raise TypeError(
                f"ticket_type must be one of: {','.join(self._valid_types)}")

        if not isinstance(number_of_tickets, int):

            raise TypeError("number_of_tickets must be an integer")

        #Because the subclasses __setattr__ method has been overwrited
        #we tell the init method to call the __setattr__ method of the superclass
        super().__setattr__("ticket_type", ticket_type)
        super().__setattr__("number_of_tickets", number_of_tickets)

    def __setattr__(self, __name, __value):
        raise AssertionError(f"Instances of TicketTypeRequest cannot be modified after instansiation")

    def get_ticket_type(self):

        return self.ticket_type

    def get_tickets_number(self):

        return self.number_of_tickets