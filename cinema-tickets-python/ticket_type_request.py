from dataclasses import dataclass


VALID_TICKET_TYPES = ("ADULT", "CHILD", "INFANT")


@dataclass(frozen=True)
class TicketTypeRequest:
    ticket_type: str
    number_of_tickets: int

    def __post_init__(self):
        if not isinstance(self.ticket_type, str):
            raise TypeError("ticket_type must be a string")

        if self.ticket_type not in VALID_TICKET_TYPES:
            raise TypeError(f"ticket_type must be one of: {','.join(VALID_TICKET_TYPES)}")

        if not isinstance(self.number_of_tickets, int):
            raise TypeError("number_of_tickets must be an integer")

        if not self.number_of_tickets >= 0:
            raise ValueError("number_of_tickets must be positive")

    def get_ticket_type(self):
        return self.ticket_type

    def get_tickets_number(self):
        return self.number_of_tickets
