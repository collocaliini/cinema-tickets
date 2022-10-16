from unittest import TestCase
from unittest.mock import call, patch

from purchase_exceptions import InvalidPurchaseException
from ticket_service import TicketService


class TestTicketService(TestCase):
    ticket_service = TicketService()

    @patch('ticket_service.TicketPaymentService')
    @patch('ticket_service.SeatReservationService')
    def test_purchase_tickets_0(self, seat_reservation_mock, ticket_payment_mock):
        self.ticket_service.purchase_tickets(763, {"ADULT": 3, "CHILD": 5, "INFANT": 2})
        seat_reservation_mock.assert_has_calls([call().reserve_seat(763, 8)])
        ticket_payment_mock.assert_has_calls([call().make_payment(763, 110)])

    @patch('ticket_service.TicketPaymentService')
    @patch('ticket_service.SeatReservationService')
    def test_purchase_tickets_1(self, seat_reservation_mock, ticket_payment_mock):
        self.ticket_service.purchase_tickets(10001110101, {"CHILD": 5, "ADULT": 6})
        seat_reservation_mock.assert_has_calls([call().reserve_seat(10001110101, 11)])
        ticket_payment_mock.assert_has_calls([call().make_payment(10001110101, 170)])

    @patch('ticket_service.TicketPaymentService')
    @patch('ticket_service.SeatReservationService')
    def test_purchase_tickets_2(self, seat_reservation_mock, ticket_payment_mock):
        self.ticket_service.purchase_tickets(1, {"ADULT": 19})
        seat_reservation_mock.assert_has_calls([call().reserve_seat(1, 19)])
        ticket_payment_mock.assert_has_calls([call().make_payment(1, 380)])

    @patch('ticket_service.TicketPaymentService')
    @patch('ticket_service.SeatReservationService')
    def test_purchase_tickets_3(self, seat_reservation_mock, ticket_payment_mock):
        self.ticket_service.purchase_tickets(763, {"ADULT": 7, "CHILD": 8, "INFANT": 5})
        seat_reservation_mock.assert_has_calls([call().reserve_seat(763, 15)])
        ticket_payment_mock.assert_has_calls([call().make_payment(763, 220)])

    def test_purchase_tickets_bad_account(self):
        with self.assertRaises(TypeError):
            self.ticket_service.purchase_tickets("hello", {"ADULT": 3})

        with self.assertRaises(ValueError):
            self.ticket_service.purchase_tickets(-34, {"ADULT": 3})

    def test_purchase_tickets_bad_tickets(self):
        with self.assertRaises(ValueError):
            self.ticket_service.purchase_tickets(17, {"ADULT": -1, "CHILD": 1})

    def test_purchase_tickets_no_tickets(self):
        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {})

        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"ADULT": 0, "CHILD": 0, "INFANT": 0})

    def test_purchase_tickets_too_many_tickets(self):
        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"ADULT": 10, "CHILD": 11, "INFANT": 12})

        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"ADULT": 33})

    def test_purchase_tickets_no_adults(self):
        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"CHILD": 5, "INFANT": 7})

        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"CHILD": 8})

    def test_purchase_tickets_too_many_infants(self):
        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"ADULT": 5, "CHILD": 6, "INFANT": 6})

        with self.assertRaises(InvalidPurchaseException):
            self.ticket_service.purchase_tickets(17, {"ADULT": 5, "INFANT": 9})
