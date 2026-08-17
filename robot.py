class Robot:
    manufacturer = "Ritwal"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

if __name__ == "__main__":
    r1 = Robot("Bot1")
    r2 = Robot("Bot2")
    print(r1.name)
    print(r1.battery)
    print(Robot.population)
    print(r1.manufacturer)