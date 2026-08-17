class Robot:
    manufacturer = "Ritwal"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            self._battery = 0
        elif value > 100:
            self._battery = 100
        else:
            self._battery = value

if __name__ == "__main__":
    r1 = Robot("Bot1", battery=150)
    r2 = Robot("Bot2", battery=-20)
    print(r1.battery)
    print(r2.battery)
    print(Robot.population)