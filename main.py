import datetime

# User and Role Classes
class Role:
    PASSENGER = 'Passenger'
    STAFF = 'Staff'
    ADMIN = 'Admin'

class User:
    def __init__(self, user_id, surname, name, address, phone, role, password):
        self.user_id = user_id
        self.surname = surname
        self.name = name
        self.address = address
        self.phone = phone
        self.role = role
        self.password = password
        self.bookings = []
        if role == Role.PASSENGER:
            self.passenger = Passenger(user_id, surname, name, address, phone)
        elif role == Role.STAFF:
            self.staff = Staff(user_id, surname, name, address, phone, 0, role, None)
        else:
            self.passenger = None
            self.staff = None

    def update_profile(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
        print(f"User {self.user_id} profile updated.")
        if self.role == Role.PASSENGER and self.passenger:
            self.passenger.update_profile(name, address, phone)
        elif self.role == Role.STAFF and self.staff:
            self.staff.update_personal_info(name, address, phone)

class Passenger:
    def __init__(self, passenger_id, surname, name, address, phone):
        self.passenger_id = passenger_id
        self.surname = surname
        self.name = name
        self.address = address
        self.phone = phone
        self.bookings = []

    def create_account(self):
        print(f"Account created for passenger {self.name}.")

    def login(self):
        print(f"Passenger {self.name} logged in.")

    def logout(self):
        print(f"Passenger {self.name} logged out.")

    def bookFlight(self, flight):
        booking = Booking(self, flight)
        self.bookings.append(booking)
        flight.bookings.append(booking)
        print(f"Passenger {self.name} booked flight {flight.flight_num}.")
        return booking

    def checkFlightStatus(self, flight):
        print(f"Flight {flight.flight_num} status: {flight.status}.")
        return flight.status

    def trackLoyaltyStatus(self, loyalty_program_service):
        status = loyalty_program_service.get_loyalty_status(self.passenger_id)
        print(f"Loyalty status for passenger {self.name}: {status}.")
        return status

    def notifyPassenger(self, notification_service, message):
        notification_service.notify(self.passenger_id, message)

    def update_profile(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
        print(f"Passenger {self.passenger_id} profile updated.")

    def view_booking_history(self):
        print(f"Booking history for {self.name}: {[b.flight.flight_num for b in self.bookings]}")
        return self.bookings

class Booking:
    def __init__(self, passenger, flight):
        self.passenger = passenger
        self.flight = flight
        self.seat = None

    def cancel_booking(self):
        self.passenger.bookings.remove(self)
        self.flight.bookings.remove(self)
        print(f"Booking for flight {self.flight.flight_num} canceled.")

    def change_seat(self, new_seat):
        if new_seat in self.flight.available_seats:
            self.seat = new_seat
            return True
        return False

class Flight:
    def __init__(self, flight_num, origin, dest, date, arr_time, dep_time):
        self.flight_num = flight_num
        self.origin = origin
        self.dest = dest
        self.date = date
        self.arr_time = arr_time
        self.dep_time = dep_time
        self.bookings = []
        self.staff = []
        self.aircraft = None
        self.available_seats = set(range(1, 201))  # Assuming 200 seats per flight
        self.route = Route(origin, dest)
        self.status = "Scheduled"

    def updateFlightDetails(self, new_details):
        self.origin = new_details.get("origin", self.origin)
        self.dest = new_details.get("dest", self.dest)
        self.date = new_details.get("date", self.date)
        self.arr_time = new_details.get("arr_time", self.arr_time)
        self.dep_time = new_details.get("dep_time", self.dep_time)
        self.status = new_details.get("status", self.status)
        print(f"Flight {self.flight_num} details updated.")

    def addPassenger(self, passenger):
        booking = Booking(passenger, self)
        self.bookings.append(booking)
        passenger.bookings.append(booking)
        print(f"Passenger {passenger.name} added to flight {self.flight_num}.")

    def assignAirplane(self, airplane):
        self.aircraft = airplane
        print(f"Aircraft {airplane.serial_num} allocated to flight {self.flight_num}.")

    def assign_staff(self, staff, role):
        flight_staff = FlightStaff(self, staff, role)
        self.staff.append(flight_staff)
        print(f"Staff {staff.name} assigned to flight {self.flight_num} as {role}.")
        return flight_staff

    def update_status(self, new_status):
        self.status = new_status
        print(f"Flight {self.flight_num} status updated to {new_status}.")

    def add_intermediate_stop(self, city):
        self.route.add_intermediate_city(city)
        print(f"Added intermediate stop in {city.name} for flight {self.flight_num}.")

    def remove_intermediate_stop(self, city):
        self.route.remove_intermediate_city(city)
        print(f"Removed intermediate stop in {city.name} for flight {self.flight_num}.")

class FlightStaff:
    def __init__(self, flight, staff, role):
        self.flight = flight
        self.staff = staff
        self.role = role

    def change_role(self, new_role):
        self.role = new_role
        print(f"Role changed to {new_role} for staff {self.staff.name} on flight {self.flight.flight_num}.")

class Airplane:
    def __init__(self, serial_num, manufacturer, model):
        self.serial_num = serial_num
        self.manufacturer = manufacturer
        self.model = model

    def updateDetails(self, new_details):
        self.manufacturer = new_details.get("manufacturer", self.manufacturer)
        self.model = new_details.get("model", self.model)
        print(f"Airplane {self.serial_num} details updated.")

    def schedule_maintenance(self, date):
        self.maintenance_date = date
        print(f"Airplane {self.serial_num} scheduled for maintenance on {date}.")

class Staff:
    def __init__(self, emp_num, surname, name, address, phone, salary, role, type_rating):
        self.emp_num = emp_num
        self.surname = surname
        self.name = name
        self.address = address
        self.phone = phone
        self.salary = salary
        self.role = role
        self.type_rating = type_rating

    def assignToFlight(self, flight):
        flight.assign_staff(self, self.role)
        print(f"Staff {self.name} assigned to flight {flight.flight_num} as {self.role}.")

    def updateDetails(self, new_details):
        self.name = new_details.get("name", self.name)
        self.address = new_details.get("address", self.address)
        self.phone = new_details.get("phone", self.phone)
        self.salary = new_details.get("salary", self.salary)
        self.role = new_details.get("role", self.role)
        self.type_rating = new_details.get("type_rating", self.type_rating)
        print(f"Staff {self.emp_num} details updated.")

    def update_personal_info(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def request_salary_change(self, new_salary):
        self.salary = new_salary
        print(f"Salary for staff {self.name} updated to {new_salary}.")

    def assign_type_rating(self, rating):
        self.type_rating = rating
        print(f"Type rating {rating} assigned to staff {self.name}.")

class City:
    def __init__(self, city_id, name, airport):
        self.city_id = city_id
        self.name = name
        self.airport = airport
        self.flights = []

    def addFlight(self, flight):
        self.flights.append(flight)
        print(f"Flight {flight.flight_num} added to city {self.name}.")

    def getFlights(self):
        return self.flights

    def add_flight(self, flight):
        self.flights.append(flight)
        print(f"Flight {flight.flight_num} added to city {self.name}.")

    def remove_flight(self, flight):
        self.flights.remove(flight)
        print(f"Flight {flight.flight_num} removed from city {self.name}.")

class Route:
    def __init__(self, origin, dest):
        self.origin = origin
        self.dest = dest
        self.intermediate_cities = []

    def add_intermediate_city(self, city):
        self.intermediate_cities.append(city)
        print(f"City {city.name} added as intermediate stop between {self.origin} and {self.dest}.")

    def remove_intermediate_city(self, city):
        self.intermediate_cities.remove(city)
        print(f"City {city.name} removed as intermediate stop between {self.origin} and {self.dest}.")

class PassengerRepository:
    def __init__(self):
        self.passengers = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"Passenger {passenger.name} added to repository.")

    def get_passenger(self, user_id):
        for user in self.passengers:
            if isinstance(user, User) and user.user_id == user_id:
                return user
        return None

class FlightRepository:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)
        print(f"Flight {flight.flight_num} added to repository.")

    def get_flight(self, flight_num):
        for flight in self.flights:
            if flight.flight_num == flight_num:
                return flight
        return None

class StaffRepository:
    def __init__(self):
        self.staff = []

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Staff {staff_member.name} added to repository.")

    def get_staff(self, emp_num):
        for user in self.staff:
            if isinstance(user, Staff) and user.emp_num == emp_num:
                return user
        return None

class AirplaneRepository:
    def __init__(self):
        self.airplanes = []

    def add_airplane(self, airplane):
        self.airplanes.append(airplane)
        print(f"Airplane {airplane.serial_num} added to repository.")

    def get_airplane(self, serial_num):
        for airplane in self.airplanes:
            if airplane.serial_num == serial_num:
                return airplane
        return None

class CityRepository:
    def __init__(self):
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)
        print(f"City {city.name} added to repository.")

    def get_city(self, city_id):
        for city in self.cities:
            if city.city_id == city_id:
                return city
        return None

    def remove_city(self, city):
        self.cities.remove(city)
        print(f"City {city.name} removed from repository.")

# Services
class LoyaltyProgramService:
    def __init__(self):
        self.programs = []

    def updateLoyaltyStatus(self):
        # Logic to update loyalty status
        pass

    def getRewards(self):
        # Logic to get rewards
        pass

    def get_loyalty_status(self, passenger_id):
        # Mock loyalty status
        return "Gold"

class NotificationService:
    def __init__(self):
        self.services = []

    def notifyPassenger(self, passenger_id, message):
        print(f"Notification sent to passenger {passenger_id}: {message}")

# Controllers for role-specific actions
class PassengerController:
    def __init__(self, passenger_repository, flight_repository, loyalty_program_service, notification_service):
        self.passenger_repository = passenger_repository
        self.flight_repository = flight_repository
        self.loyalty_program_service = loyalty_program_service
        self.notification_service = notification_service

    def bookFlight(self, user, flight_num):
        if user.role != Role.PASSENGER:
            print("Access denied: Only passengers can book flights.")
            return None
        passenger = self.passenger_repository.get_passenger(user.user_id)
        flight = self.flight_repository.get_flight(flight_num)
        if passenger and flight:
            booking = passenger.passenger.bookFlight(flight)
            return booking
        return None

    def view_booking_history(self, user):
        if user.role != Role.PASSENGER:
            print("Access denied: Only passengers can view booking history.")
            return []
        passenger = self.passenger_repository.get_passenger(user.user_id)
        if passenger:
            return passenger.passenger.view_booking_history()
        return []

    def checkFlightStatus(self, user, flight_num):
        flight = self.flight_repository.get_flight(flight_num)
        if flight:
            return flight.status
        return None

    def trackLoyaltyStatus(self, user):
        if user.role != Role.PASSENGER:
            print("Access denied: Only passengers can track loyalty status.")
            return None
        passenger = self.passenger_repository.get_passenger(user.user_id)
        if passenger:
            return passenger.passenger.trackLoyaltyStatus(self.loyalty_program_service)
        return None

    def notifyPassenger(self, user, message):
        if user.role != Role.PASSENGER:
            print("Access denied: Only passengers can receive notifications.")
            return None
        passenger = self.passenger_repository.get_passenger(user.user_id)
        if passenger:
            passenger.passenger.notifyPassenger(self.notification_service, message)
            return True
        return False

class StaffController:
    def __init__(self, flight_repository, staff_repository):
        self.flight_repository = flight_repository
        self.staff_repository = staff_repository

    def assignToFlight(self, user, flight_num, emp_num, role):
        if user.role != Role.STAFF and user.role != Role.ADMIN:
            print("Access denied: Only staff or admin can assign staff.")
            return None
        flight = self.flight_repository.get_flight(flight_num)
        staff_member = self.staff_repository.get_staff(emp_num)
        if flight and staff_member:
            assigned_staff = flight.assign_staff(staff_member.staff, role)
            print(f"Assigned staff {staff_member.surname} to flight {flight_num} as {role}.")
            return assigned_staff
        return None

    def view_flight_details(self, user, flight_num):
        if user.role != Role.STAFF:
            print("Access denied: Only staff can view flight details.")
            return None
        flight = self.flight_repository.get_flight(flight_num)
        if flight:
            print(f"Flight details for flight {flight_num}: Origin {flight.origin}, Destination {flight.dest}, Date {flight.date}, Arrival Time {flight.arr_time}, Departure Time {flight.dep_time}.")
            return flight
        return None

class AdminController:
    def __init__(self, flight_repository, airplane_repository, city_repository, passenger_repository, staff_repository):
        self.flight_repository = flight_repository
        self.airplane_repository = airplane_repository
        self.city_repository = city_repository
        self.passenger_repository = passenger_repository
        self.staff_repository = staff_repository

    def managePassengerDetails(self, passenger_id, new_details):
        passenger = self.passenger_repository.get_passenger(passenger_id)
        if passenger:
            passenger.update_profile(new_details.get("name", passenger.name),
                                     new_details.get("address", passenger.address),
                                     new_details.get("phone", passenger.phone))
            print(f"Passenger details for {passenger_id} updated.")
        else:
            print("Passenger not found.")

    def manageFlightInformation(self, flight_num, new_details):
        flight = self.flight_repository.get_flight(flight_num)
        if flight:
            flight.updateFlightDetails(new_details)
            print(f"Flight information for {flight_num} updated.")
        else:
            print("Flight not found.")

    def manageStaffDetails(self, staff_id, new_details):
        staff = self.staff_repository.get_staff(staff_id)
        if staff:
            staff.updateDetails(new_details)
            print(f"Staff details for {staff_id} updated.")
        else:
            print("Staff not found.")

    def manageAirplaneDetails(self, serial_num, new_details):
        airplane = self.airplane_repository.get_airplane(serial_num)
        if airplane:
            airplane.updateDetails(new_details)
            print(f"Airplane details for {serial_num} updated.")
        else:
            print("Airplane not found.")

    def manageCityDetails(self, city_id, new_details):
        city = self.city_repository.get_city(city_id)
        if city:
            city.name = new_details.get("name", city.name)
            city.airport = new_details.get("airport", city.airport)
            print(f"City details for {city_id} updated.")
        else:
            print("City not found.")

    def generateReports(self):
        print("Generating reports...")

    def searchAndFilter(self):
        print("Searching and filtering data...")

    def allocate_aircraft(self, user, flight_num, serial_num):
        if user.role != Role.ADMIN:
            print("Access denied: Only admin can allocate aircraft.")
            return None
        flight = self.flight_repository.get_flight(flight_num)
        airplane = self.airplane_repository.get_airplane(serial_num)
        if flight and airplane:
            flight.assignAirplane(airplane)
            return airplane
        return None

    def update_flight_status(self, user, flight_num, new_status):
        if user.role != Role.ADMIN:
            print("Access denied: Only admin can update flight status.")
            return None
        flight = self.flight_repository.get_flight(flight_num)
        if flight:
            flight.update_status(new_status)
            return flight
        return None

    def add_city(self, user, city):
        if user.role != Role.ADMIN:
            print("Access denied: Only admin can add cities.")
            return None
        self.city_repository.add_city(city)
        print(f"City {city.name} added.")

    def remove_city(self, user, city_id):
        if user.role != Role.ADMIN:
            print("Access denied: Only admin can remove cities.")
            return None
        city = self.city_repository.get_city(city_id)
        if city:
            self.city_repository.remove_city(city)
            print(f"City {city.name} removed.")
        else:
            print("City not found.")

def initialize_data():
    # Repositories
    passenger_repo = PassengerRepository()
    flight_repo = FlightRepository()
    staff_repo = StaffRepository()
    airplane_repo = AirplaneRepository()
    city_repo = CityRepository()

    # Services
    loyalty_program_service = LoyaltyProgramService()
    notification_service = NotificationService()

    # Controllers
    passenger_controller = PassengerController(passenger_repo, flight_repo, loyalty_program_service, notification_service)
    staff_controller = StaffController(flight_repo, staff_repo)
    admin_controller = AdminController(flight_repo, airplane_repo, city_repo, passenger_repo, staff_repo)

    # Sample Data
    admin = User(3, "Admin", "Super", "789 Pine St", "123123123", Role.ADMIN, "adminpass")
    passenger_repo.add_passenger(admin)  # Add the admin user to the passenger repository

    print("Contents of passenger_repo after adding admin user:")
    for user in passenger_repo.passengers:
        print(f"User ID: {user.user_id}, Name: {user.name}, Role: {user.role}")

    passenger = User(1, "Doe", "John", "123 Main St", "123456789", Role.PASSENGER, "pass123")
    passenger_repo.add_passenger(passenger)

    staff = User(2, "Smith", "Alice", "456 Birch St", "987654321", Role.STAFF, "staffpass")
    staff_repo.add_staff(staff)

    flight = Flight(1, "LHR", "JFK", datetime.date(2023, 6, 1), "10:00", "14:00")
    flight_repo.add_flight(flight)

    airplane = Airplane("1234", "Boeing", "737")
    airplane_repo.add_airplane(airplane)

    city = City(1, "Boston", "BOS")
    city_repo.add_city(city)

    return passenger_controller, staff_controller, admin_controller, passenger_repo, staff_repo

# This main function is just to demonstrate the usage
def main():
    passenger_controller, staff_controller, admin_controller, passenger_repo, staff_repo = initialize_data()

    # Get the admin user from the repository
    admin = passenger_repo.get_passenger(3)

    print("\nPassenger Actions:")
    passenger = User(1, "Doe", "John", "123 Main St", "123456789", Role.PASSENGER, "pass123")
    passenger_repo.add_passenger(passenger)
    passenger_controller.bookFlight(passenger, 1)
    passenger_controller.view_booking_history(passenger)

    print("\nStaff Actions:")
    staff = User(2, "Smith", "Alice", "456 Birch St", "987654321", Role.STAFF, "staffpass")
    staff_repo.add_staff(staff)
    staff_controller.view_flight_details(staff, 1)
    staff_controller.assignToFlight(staff, 1, staff.user_id, "Pilot")

    print("\nAdmin Actions:")
    admin_controller.allocate_aircraft(admin, 1, "1234")
    admin_controller.update_flight_status(admin, 1, "Delayed")
    admin_controller.add_city(admin, City(2, "Chicago", "ORD"))
    admin_controller.remove_city(admin, 1)

if __name__ == "__main__":
    main()
