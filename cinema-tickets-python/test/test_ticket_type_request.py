from unittest import TestCase

from hypothesis import assume, given
from hypothesis.strategies import integers, sampled_from, text

from ticket_type_request import TicketTypeRequest


VALID_TICKET_TYPES = ("ADULT", "CHILD", "INFANT")


class TestTicketTypeRequest(TestCase):
    @given(sampled_from(VALID_TICKET_TYPES), integers(min_value=0))
    def test_init(self, ticket_type, number_of_tickets):
        TicketTypeRequest(ticket_type, number_of_tickets)

    @given(sampled_from(VALID_TICKET_TYPES), text())
    def test_init_number_type_error(self, ticket_type, number_of_tickets):
        with self.assertRaises(TypeError):
            TicketTypeRequest(ticket_type, number_of_tickets)

    @given(sampled_from(VALID_TICKET_TYPES), integers(max_value=-1))
    def test_init_number_value_error(self, ticket_type, number_of_tickets):
        with self.assertRaises(ValueError):
            TicketTypeRequest(ticket_type, number_of_tickets)

    @given(text(), integers(min_value=0))
    def test_init_ticket_type_error(self, ticket_type, number_of_tickets):
        assume(ticket_type not in VALID_TICKET_TYPES)
        with self.assertRaises(TypeError):
            TicketTypeRequest(ticket_type, number_of_tickets)
