from unittest import TestCase

from ticket_information_service import TicketInformationService
from ticket_type_request import TicketTypeRequest


class TestTicketInformationService(TestCase):
    ticket_information_service = TicketInformationService()

    def test_get_ticket_type_price(self):
        request = TicketTypeRequest("ADULT", 3)
        result = self.ticket_information_service.get_ticket_type_price(request)
        self.assertEqual(result, 20)

        request = TicketTypeRequest("CHILD", 5)
        result = self.ticket_information_service.get_ticket_type_price(request)
        self.assertEqual(result, 10)

        request = TicketTypeRequest("INFANT", 2)
        result = self.ticket_information_service.get_ticket_type_price(request)
        self.assertEqual(result, 0)

    def test_get_ticket_type_seat_required(self):
        request = TicketTypeRequest("ADULT", 3)
        result = self.ticket_information_service.get_ticket_type_seat_required(request)
        self.assertEqual(result, True)

        request = TicketTypeRequest("CHILD", 5)
        result = self.ticket_information_service.get_ticket_type_seat_required(request)
        self.assertEqual(result, True)

        request = TicketTypeRequest("INFANT", 2)
        result = self.ticket_information_service.get_ticket_type_seat_required(request)
        self.assertEqual(result, False)

    def test_get_total_price(self):
        request = TicketTypeRequest("ADULT", 3)
        result = self.ticket_information_service.get_total_price(request)
        self.assertEqual(result, 60)

        request = TicketTypeRequest("CHILD", 5)
        result = self.ticket_information_service.get_total_price(request)
        self.assertEqual(result, 50)

        request = TicketTypeRequest("INFANT", 2)
        result = self.ticket_information_service.get_total_price(request)
        self.assertEqual(result, 0)

    def test_get_total_seats(self):
        request = TicketTypeRequest("ADULT", 3)
        result = self.ticket_information_service.get_total_seats(request)
        self.assertEqual(result, 3)

        request = TicketTypeRequest("CHILD", 5)
        result = self.ticket_information_service.get_total_seats(request)
        self.assertEqual(result, 5)

        request = TicketTypeRequest("INFANT", 2)
        result = self.ticket_information_service.get_total_seats(request)
        self.assertEqual(result, 0)
