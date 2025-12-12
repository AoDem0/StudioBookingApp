import Data_Man as dm


class Booking_Data(dm.Database_Management):
    def __init__(self, filename="database.json"):
        super().__init__(filename)

    def create_reservation(self, studio_id, username, date, time_from, time_to, status="pending", equipment=None):
        """Create a new reservation"""
        if equipment is None:
            equipment = []
            
        data = self.load_data()
        if "reservations" not in data:
            data["reservations"] = []
        
        # Generate new reservation ID
        reservation_id = self.next_reservation_id()
        
        new_reservation = {
            "id": reservation_id,
            "studio_id": studio_id,
            "username": username,
            "date": date,
            "time_from": time_from,
            "time_to": time_to,
            "status": status,  # pending, approved, rejected, cancelled
            "equipment": equipment
        }
        
        data["reservations"].append(new_reservation)
        self.save_data(data)
        return True

    def get_all_reservations(self):
        """Get all reservations"""
        data = self.load_data()
        return data.get("reservations", [])

    def get_user_reservations(self, username):
        """Get reservations for a specific user"""
        data = self.load_data()
        reservations = data.get("reservations", [])
        return [r for r in reservations if r.get("username") == username]

    def get_studio_reservations(self, studio_id):
        """Get reservations for a specific studio"""
        data = self.load_data()
        reservations = data.get("reservations", [])
        return [r for r in reservations if r.get("studio_id") == studio_id]

    def update_reservation_status(self, reservation_id, new_status):
        """Update reservation status (pending, approved, rejected, cancelled)"""
        data = self.load_data()
        reservations = data.get("reservations", [])
        
        for reservation in reservations:
            if reservation["id"] == reservation_id:
                reservation["status"] = new_status
                self.save_data(data)
                return True
        return False

    def remove_reservation(self, reservation_id):
        """Delete a reservation by ID"""
        data = self.load_data()
        if "reservations" not in data:
            return False

        for i, reservation in enumerate(data["reservations"]):
            if reservation["id"] == reservation_id:
                del data["reservations"][i]
                self.save_data(data)
                return True
        return False

    def update_reservation(self, reservation_id, date=None, time_from=None, time_to=None):
        """Update reservation details"""
        data = self.load_data()
        reservations = data.get("reservations", [])
        
        for reservation in reservations:
            if reservation["id"] == reservation_id:
                if date:
                    reservation["date"] = date
                if time_from:
                    reservation["time_from"] = time_from
                if time_to:
                    reservation["time_to"] = time_to
                self.save_data(data)
                return True
        return False

    def next_reservation_id(self):
        """Generate next available reservation ID"""
        data = self.load_data()
        if "reservations" not in data or not data["reservations"]:
            return 1
        max_id = max([r["id"] for r in data["reservations"]], default=0)
        return max_id + 1

    def check_availability(self, studio_id, date, time_from, time_to):
        """Check if a studio is available at given time"""
        data = self.load_data()
        reservations = data.get("reservations", [])
        
        for reservation in reservations:
            if (reservation["studio_id"] == studio_id and 
                reservation["date"] == date and 
                reservation["status"] in ["pending", "approved"]):
                # Check for time overlap
                if not (time_to <= reservation["time_from"] or time_from >= reservation["time_to"]):
                    return False
        return True