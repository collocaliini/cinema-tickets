from ticket_type_request import TicketTypeRequest


class TicketInformationService:
    """Service class for providing pricing and reservation rules for tickets"""

    _ticket_type_prices = {
        "ADULT": 20,
        "CHILD": 10,
        "INFANT": 0,
    }

    _ticket_type_seat_required = {
        "ADULT": True,
        "CHILD": True,
        "INFANT": False,
    }

    def get_ticket_type_price(self, ticket_type_request: TicketTypeRequest) -> int:
        return self._ticket_type_prices[ticket_type_request.ticket_type]

    def get_ticket_type_seat_required(self, ticket_type_request: TicketTypeRequest) -> bool:
        return self._ticket_type_seat_required[ticket_type_request.ticket_type]

    def get_total_price(self, ticket_type_request: TicketTypeRequest) -> int:
        return self.get_ticket_type_price(ticket_type_request) * ticket_type_request.number_of_tickets

    def get_total_seats(self, ticket_type_request: TicketTypeRequest) -> int:
        if self.get_ticket_type_seat_required(ticket_type_request):
            return ticket_type_request.number_of_tickets
        return 0
