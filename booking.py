# booking.py
# ─────────────────────────────────────────────
#  BOOKING BUSINESS LOGIC
# ─────────────────────────────────────────────

import uuid
from storage import load, save, BOOKINGS_FILE
from vehicle import get_vehicle


def create_booking(customer_username: str, vehicle_type: str,
                   start: str, end: str, distance: float) -> dict:
    """
    Calculate the fare, build a booking record, persist it, and return it.
    Raises ValueError if vehicle_type is unknown or distance is invalid.
    """
    if distance <= 0:
        raise ValueError("Distance must be greater than 0.")

    vehicle   = get_vehicle(vehicle_type)
    fare_cost = round(vehicle.calculate_cost(distance), 2)

    booking = {
        "booking_id":      str(uuid.uuid4())[:8],
        "customer":        customer_username,
        "vehicle_type":    vehicle_type,
        "start":           start,
        "end":             end,
        "distance":        distance,
        "total_cost":      fare_cost,
        "status":          "Pending",
        "assigned_rider":  "None",
    }

    all_bookings = load(BOOKINGS_FILE)
    all_bookings.append(booking)
    save(BOOKINGS_FILE, all_bookings)

    return booking


def get_user_bookings(username: str) -> list:
    """Return all bookings belonging to the given customer username."""
    return [b for b in load(BOOKINGS_FILE) if b["customer"] == username]


def get_pending_bookings_for_vehicle(vehicle_type: str) -> list:
    """Return all Pending bookings that match the given vehicle type.
    'Bike' and 'Motorcycle' are treated as the same vehicle class.
    """
    _MOTO_ALIASES = {"Bike", "Motorcycle"}
    if vehicle_type in _MOTO_ALIASES:
        return [
            b for b in load(BOOKINGS_FILE)
            if b["status"] == "Pending" and b["vehicle_type"] in _MOTO_ALIASES
        ]
    return [
        b for b in load(BOOKINGS_FILE)
        if b["status"] == "Pending" and b["vehicle_type"] == vehicle_type
    ]


def get_rider_bookings(rider_username: str) -> list:
    """Return all bookings assigned to the given rider."""
    return [b for b in load(BOOKINGS_FILE) if b["assigned_rider"] == rider_username]


def assign_booking(booking_id: str, rider_username: str) -> bool:
    """
    Mark a booking as Assigned and record the rider.
    Returns True if the booking was found and updated, False if not found
    or if the rider is currently marked offline/unavailable.
    """
    from storage import RIDERS_FILE
    riders = load(RIDERS_FILE)
    rider = next((r for r in riders if r["username"] == rider_username), None)
    if rider is not None and not rider.get("available", True):
        return False

    all_bookings = load(BOOKINGS_FILE)
    for item in all_bookings:
        if item["booking_id"] == booking_id:
            item["status"]          = "Assigned"
            item["assigned_rider"]  = rider_username
            save(BOOKINGS_FILE, all_bookings)
            return True
    return False


def cancel_booking(booking_id: str, customer_username: str) -> bool:
    """
    Cancel a booking belonging to the given customer.
    Only Pending bookings can be cancelled (Assigned rides already have a rider en route).
    Returns True if cancelled, False if not found / not owned / not cancellable.
    """
    all_bookings = load(BOOKINGS_FILE)
    for item in all_bookings:
        if item["booking_id"] == booking_id and item["customer"] == customer_username:
            if item["status"] != "Pending":
                return False
            item["status"] = "Cancelled"
            save(BOOKINGS_FILE, all_bookings)
            return True
    return False


def complete_booking(booking_id: str, rider_username: str) -> bool:
    """
    Mark a booking as Completed by the rider it was assigned to.
    Returns True if completed, False if not found / not owned / not assigned.
    """
    all_bookings = load(BOOKINGS_FILE)
    for item in all_bookings:
        if item["booking_id"] == booking_id and item["assigned_rider"] == rider_username:
            if item["status"] != "Assigned":
                return False
            item["status"] = "Completed"
            save(BOOKINGS_FILE, all_bookings)
            return True
    return False