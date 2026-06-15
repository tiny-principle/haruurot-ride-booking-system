# vehicle.py
# ─────────────────────────────────────────────
#  VEHICLE CLASS POLYMORPHISM (Pricing Engines)
# ─────────────────────────────────────────────


class Vehicle:
    """Base vehicle with a configurable fare structure."""

    def __init__(self, base_fare: float, per_mile: float):
        self.base_fare = base_fare
        self.per_mile  = per_mile

    def calculate_cost(self, distance: float) -> float:
        """Return total fare for the given distance in miles."""
        return self.base_fare + (self.per_mile * distance)


class Car(Vehicle):
    def __init__(self):
        super().__init__(base_fare=5.00, per_mile=2.50)


class Van(Vehicle):
    def __init__(self):
        super().__init__(base_fare=8.00, per_mile=4.00)


class Bike(Vehicle):
    def __init__(self):
        super().__init__(base_fare=3.00, per_mile=1.50)


# Convenience lookup so screens don't need to import each class individually
VEHICLE_MAP = {
    "Car":        Car,
    "Van":        Van,
    "Bike":       Bike,   # kept for backward-compat with stored bookings/riders
    "Motorcycle": Bike,   # display name used in the UI going forward
}


def get_vehicle(vehicle_type: str) -> Vehicle:
    """Instantiate and return the correct Vehicle subclass by name."""
    cls = VEHICLE_MAP.get(vehicle_type)
    if cls is None:
        raise ValueError(f"Unknown vehicle type: {vehicle_type!r}")
    return cls()