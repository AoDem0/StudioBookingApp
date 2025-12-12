import Data_Man as dm


class Studio_Data(dm.Database_Management):
    def __init__(self, filename="database.json"):
        super().__init__(filename)

    def register_studio(self, id, name, city, price):
        data = self.load_data()
        if "studios" not in data:
            data["studios"] = []
        for u in data["studios"]:
            if u["name"] == name:
                return False 
        new_room = {
            "id": id,
            "name": name,
            "city": city,
            "price_for_h": price,
            "equipment": []
        }
        data["studios"].append(new_room)
        self.save_data(data)
        return True
    
    def remove_studio(self, id):
        data = self.load_data()
        if "studios" not in data:
            return False  # brak studiów do usunięcia

        for i, studio in enumerate(data["studios"]):
            if (id is not None and studio["id"] == id):
                del data["studios"][i]  
                self.save_data(data)
                return True

        return False
    
    def next_id(self):
        data = self.load_data()
        if "studios" not in data:
            return 0
        max_id = max([s["id"] for s in data["studios"]], default=-1)
        return max_id + 1