# HARUUROT Ride Booking System

> **Ride Fast. Ride Safe. Ride Haruurot!**

A Python-based desktop ride booking system developed as a final project for **CMPE 103 – Object-Oriented Programming** at the Polytechnic University of the Philippines.

---

## Developers — BSCPE 1-3

| Name | Role |
|------|------|
| Suzanne Sharrie N. Luzano | Project Manager / QA Tester |
| Gian Daniel S. Sy | Backend Developer |
| Cliff Bradley Sanchez | Backend Developer |
| Cristian M. Talidong | Backend Developer |
| Arshe Jay N. Cabildo | UI/UX Designer & Backend Developer |
| Anika Sophia C. Basa | UI/UX Designer |
| Rexchelle Ann T. Imperial | UI/UX Designer |
| Marianne E. Salvador | QA Tester |
| Stephanie Rose F. Garcia | QA Tester |

**Submitted to:** Engr. Godofredo T. Avena

---

## About the Project

HARUUROT is a desktop application that simulates a ride-hailing platform, allowing users to book rides and drivers to accept and complete trips. Built using Python and Tkinter.

### OOP Concepts Applied
- **Encapsulation** — User credentials and booking data managed through dedicated modules
- **Inheritance** — Car, Van, and Motorcycle inherit from a base `Vehicle` class
- **Polymorphism** — Fare calculation varies per vehicle type
- **Abstraction** — Complex logic hidden behind simple UI buttons

---

## Vehicle Fare Rates

| Vehicle | Base Fare | Per KM |
|---------|-----------|--------|
| Car | ₱60.00 | ₱18.00 |
| Van | ₱90.00 | ₱26.00 |
| Motorcycle | ₱40.00 | ₱12.00 |

---

## Tech Stack

- **Language:** Python 3
- **GUI:** Tkinter
- **Storage:** JSON flat files
- **Tools:** VS Code, Git, Draw.io, Canva/Figma, Google Docs

---

## How to Run

1. Make sure Python 3 is installed
2. Clone or download this repository
3. Run the app:
```bash
python main.py
```

---

## Project Structure
haruurot-ride-booking-system/

├── main.py           # App entry point & screen controller

├── auth.py           # Login & registration logic

├── booking.py        # Booking business logic

├── vehicle.py        # Vehicle classes & fare calculation

├── storage.py        # JSON file handling & password hashing

├── constants.py      # Colors, fonts, dimensions

├── widgets.py        # Reusable UI components

├── screens_auth.py   # Login/register screens

├── screens_home.py   # User & rider home screens

├── users.json        # User data store

├── riders.json       # Rider data store

└── bookings.json     # Booking records

---

## Features

- Dual-role system: Passengers and Riders
- Ride booking with vehicle selection and fare estimation
- Booking lifecycle: Pending → Assigned → Completed / Cancelled
- Cancellation fee (₱20) for assigned rides
- Persistent data storage via JSON
- Scrollable booking history / ride ledger
- Developer profiles in the Info screen
