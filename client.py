import getpass
from main import Role, User, PassengerRepository, StaffRepository, initialize_data, City


def main():
    passenger_controller, staff_controller, admin_controller, passenger_repo, staff_repo = initialize_data()

    print("Welcome to the Airline Management System")
    role = input("Enter your role (Passenger/Staff/Admin): ").strip()

    if role == Role.PASSENGER:
        passenger_id = int(input("Enter your passenger ID: ").strip())
        user = passenger_repo.get_passenger(passenger_id)
        if user:
            print(f"User found: {user.name}, Role: {user.role}")
        else:
            print("User not found in the repository.")
            return

        # Use input for password for debugging
        password = input("Enter your password: ").strip()
        if user and user.password == password and user.role == Role.PASSENGER:
            while True:
                print("\nPassenger Menu")
                print("1. Book Flight")
                print("2. View Booking History")
                print("3. Update Profile")
                print("4. Check Flight Status")
                print("5. Track Loyalty Status")
                print("6. Receive Notification")
                print("7. Exit")
                choice = input("Enter your choice: ").strip()

                if choice == '1':
                    flight_num = int(input("Enter flight number: ").strip())
                    passenger_controller.bookFlight(user, flight_num)
                elif choice == '2':
                    passenger_controller.view_booking_history(user)
                elif choice == '3':
                    name = input("Enter new name: ").strip()
                    address = input("Enter new address: ").strip()
                    phone = input("Enter new phone: ").strip()
                    user.update_profile(name, address, phone)
                elif choice == '4':
                    flight_num = int(input("Enter flight number: ").strip())
                    passenger_controller.checkFlightStatus(user, flight_num)
                elif choice == '5':
                    passenger_controller.trackLoyaltyStatus(user)
                elif choice == '6':
                    message = input("Enter notification message: ").strip()
                    passenger_controller.notifyPassenger(user, message)
                elif choice == '7':
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid credentials or role.")

    elif role == Role.STAFF:
        emp_num = int(input("Enter your employee number: ").strip())
        user = staff_repo.get_staff(emp_num)
        if user:
            print(f"User found: {user.name}, Role: {user.role}")
        else:
            print("User not found in the repository.")
            return

        # Use input for password for debugging
        password = input("Enter your password: ").strip()
        if user and user.password == password and user.role == Role.STAFF:
            while True:
                print("\nStaff Menu")
                print("1. View Flight Details")
                print("2. Assign Staff to Flight")
                print("3. Update Details")
                print("4. Exit")
                choice = input("Enter your choice: ").strip()

                if choice == '1':
                    flight_num = int(input("Enter flight number: ").strip())
                    staff_controller.view_flight_details(user, flight_num)
                elif choice == '2':
                    flight_num = int(input("Enter flight number: ").strip())
                    emp_num = int(input("Enter staff ID to assign: ").strip())
                    role = input("Enter role for the staff: ").strip()
                    staff_controller.assignToFlight(user, flight_num, emp_num, role)
                elif choice == '3':
                    new_details = {}
                    name = input("Enter new name (leave blank to keep current): ").strip()
                    address = input("Enter new address (leave blank to keep current): ").strip()
                    phone = input("Enter new phone (leave blank to keep current): ").strip()
                    if name:
                        new_details['name'] = name
                    if address:
                        new_details['address'] = address
                    if phone:
                        new_details['phone'] = phone
                    user.staff.updateDetails(new_details)
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid credentials or role.")

    elif role == Role.ADMIN:
        print("Contents of passenger_repo:")
        for user in passenger_repo.passengers:
            print(f"User ID: {user.user_id}, Name: {user.name}, Role: {user.role}")

        user_id = int(input("Enter your ID: ").strip())
        user = passenger_repo.get_passenger(user_id)
        if user:
            print(f"User found: {user.name}, Role: {user.role}")

            # Use input for password for debugging
            password = input("Enter your password: ").strip()
        else:
            print("User not found in the repository.")
            return

        if user and user.password == password and user.role == Role.ADMIN:
            while True:
                print("\nAdmin Menu")
                print("1. Manage Passenger Details")
                print("2. Manage Flight Information")
                print("3. Manage Staff Details")
                print("4. Manage Airplane Details")
                print("5. Manage City Details")
                print("6. Generate Reports")
                print("7. Search and Filter Data")
                print("8. Allocate Aircraft")
                print("9. Update Flight Status")
                print("10. Add City")
                print("11. Remove City")
                print("12. Exit")
                choice = input("Enter your choice: ").strip()

                if choice == '1':
                    passenger_id = int(input("Enter passenger ID: ").strip())
                    new_details = {}
                    name = input("Enter new name (leave blank to keep current): ").strip()
                    address = input("Enter new address (leave blank to keep current): ").strip()
                    phone = input("Enter new phone (leave blank to keep current): ").strip()
                    if name:
                        new_details['name'] = name
                    if address:
                        new_details['address'] = address
                    if phone:
                        new_details['phone'] = phone
                    admin_controller.managePassengerDetails(passenger_id, new_details)
                elif choice == '2':
                    flight_num = int(input("Enter flight number: ").strip())
                    new_details = {}
                    origin = input("Enter new origin (leave blank to keep current): ").strip()
                    dest = input("Enter new destination (leave blank to keep current): ").strip()
                    date = input("Enter new date (leave blank to keep current): ").strip()
                    arr_time = input("Enter new arrival time (leave blank to keep current): ").strip()
                    dep_time = input("Enter new departure time (leave blank to keep current): ").strip()
                    status = input("Enter new status (leave blank to keep current): ").strip()
                    if origin:
                        new_details['origin'] = origin
                    if dest:
                        new_details['dest'] = dest
                    if date:
                        new_details['date'] = date
                    if arr_time:
                        new_details['arr_time'] = arr_time
                    if dep_time:
                        new_details['dep_time'] = dep_time
                    if status:
                        new_details['status'] = status
                    admin_controller.manageFlightInformation(flight_num, new_details)
                elif choice == '3':
                    staff_id = int(input("Enter staff ID: ").strip())
                    new_details = {}
                    name = input("Enter new name (leave blank to keep current): ").strip()
                    address = input("Enter new address (leave blank to keep current): ").strip()
                    phone = input("Enter new phone (leave blank to keep current): ").strip()
                    salary = input("Enter new salary (leave blank to keep current): ").strip()
                    role = input("Enter new role (leave blank to keep current): ").strip()
                    type_rating = input("Enter new type rating (leave blank to keep current): ").strip()
                    if name:
                        new_details['name'] = name
                    if address:
                        new_details['address'] = address
                    if phone:
                        new_details['phone'] = phone
                    if salary:
                        new_details['salary'] = salary
                    if role:
                        new_details['role'] = role
                    if type_rating:
                        new_details['type_rating'] = type_rating
                    admin_controller.manageStaffDetails(staff_id, new_details)
                elif choice == '4':
                    serial_num = input("Enter airplane serial number: ").strip()
                    new_details = {}
                    manufacturer = input("Enter new manufacturer (leave blank to keep current): ").strip()
                    model = input("Enter new model (leave blank to keep current): ").strip()
                    if manufacturer:
                        new_details['manufacturer'] = manufacturer
                    if model:
                        new_details['model'] = model
                    admin_controller.manageAirplaneDetails(serial_num, new_details)
                elif choice == '5':
                    city_id = int(input("Enter city ID: ").strip())
                    new_details = {}
                    name = input("Enter new city name (leave blank to keep current): ").strip()
                    airport = input("Enter new airport code (leave blank to keep current): ").strip()
                    if name:
                        new_details['name'] = name
                    if airport:
                        new_details['airport'] = airport
                    admin_controller.manageCityDetails(city_id, new_details)
                elif choice == '6':
                    admin_controller.generateReports()
                elif choice == '7':
                    admin_controller.searchAndFilter()
                elif choice == '8':
                    flight_num = int(input("Enter flight number: ").strip())
                    serial_num = input("Enter aircraft serial number: ").strip()
                    admin_controller.allocate_aircraft(user, flight_num, serial_num)
                elif choice == '9':
                    flight_num = int(input("Enter flight number: ").strip())
                    new_status = input("Enter new flight status: ").strip()
                    admin_controller.update_flight_status(user, flight_num, new_status)
                elif choice == '10':
                    city_id = int(input("Enter city ID: ").strip())
                    name = input("Enter city name: ").strip()
                    airport = input("Enter airport code: ").strip()
                    admin_controller.add_city(user, City(city_id, name, airport))
                elif choice == '11':
                    city_id = int(input("Enter city ID to remove: ").strip())
                    admin_controller.remove_city(user, city_id)
                elif choice == '12':
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid credentials or role.")
    else:
        print("Invalid role.")


if __name__ == "__main__":
    main()
