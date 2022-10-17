from collections import Counter

from paymentgateway.ticket_payment_service import TicketPaymentService
from purchase_exceptions import InvalidPurchaseException
from seatbooking.seat_reservation_service import SeatReservationService
from ticket_information_service import TicketInformationService
from ticket_type_request import TicketTypeRequest


class TicketService:
    """Service class for purchasing tickets"""

    MAXIMUM_NUMBER_OF_TICKETS = 20

    def purchase_tickets(self, account_id: int, ticket_type_requests: dict[str, int] | list[TicketTypeRequest]) -> None:
        """Purchase tickets and reserve seats for the specified account

        account_id: can be any positive integer.
        ticket_type_requests: can be specified as a dict mapping
        ticket types ("ADULT", "CHILD", "INFANT") to number of
        tickets requested per type, or as a list of TicketTypeRequests.

        Examples:
        >>> TicketService().purchase_tickets(22910, {"ADULT": 10, "CHILD": 5, "INFANT": 3})

        >>> TicketService().purchase_tickets(
        ...     22910,
        ...     [TicketTypeRequest("ADULT", 10), TicketTypeRequest("CHILD", 5), TicketTypeRequest("INFANT", 3)],
        ... )

        """
        if isinstance(ticket_type_requests, dict):
            ticket_type_requests: list[TicketTypeRequest] = [
                TicketTypeRequest(key, value)
                for key, value in ticket_type_requests.items()
            ]

        self._validate_account(account_id)
        self._validate_tickets(ticket_type_requests)
        self._reserve_seats(account_id, ticket_type_requests)
        self._pay_for_tickets(account_id, ticket_type_requests)

    @staticmethod
    def _validate_account(account_id: int) -> None:
        if not isinstance(account_id, int):
            raise TypeError("account_id must be an integer")

        if not account_id > 0:
            raise ValueError("account_id must be greater than zero")

    def _validate_tickets(self, ticket_type_requests: list[TicketTypeRequest]) -> None:
        total_tickets_requested = sum(request.number_of_tickets for request in ticket_type_requests)

        if total_tickets_requested == 0:
            raise InvalidPurchaseException("no tickets requested")

        if total_tickets_requested > self.MAXIMUM_NUMBER_OF_TICKETS:
            raise InvalidPurchaseException(
                f"{total_tickets_requested} tickets requested, this exceeds"
                f"the maximum {self.MAXIMUM_NUMBER_OF_TICKETS} allowed"
            )

        ticket_type_counter = Counter()
        for request in ticket_type_requests:
            ticket_type_counter[request.ticket_type] += request.number_of_tickets

        if not ticket_type_counter["ADULT"]:
            raise InvalidPurchaseException("child or infant tickets requested without an adult ticket")

        if ticket_type_counter["ADULT"] < ticket_type_counter["INFANT"]:
            raise InvalidPurchaseException("more infant tickets than adult tickets requested")

    @staticmethod
    def _reserve_seats(account_id: int, ticket_type_requests: list[TicketTypeRequest]) -> None:
        ticket_information_service = TicketInformationService()

        total_seats_to_allocate = sum(
            ticket_information_service.get_total_seats(request)
            for request in ticket_type_requests
        )

        seat_reservation_service = SeatReservationService()
        seat_reservation_service.reserve_seat(account_id, total_seats_to_allocate)

    @staticmethod
    def _pay_for_tickets(account_id: int, ticket_type_requests: list[TicketTypeRequest]) -> None:
        ticket_information_service = TicketInformationService()

        total_amount_to_pay = sum(
            ticket_information_service.get_total_price(request)
            for request in ticket_type_requests
        )

        ticket_payment_service = TicketPaymentService()
        ticket_payment_service.make_payment(account_id, total_amount_to_pay)
