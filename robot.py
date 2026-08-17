import logging

logging.basicConfig(level=logging.INFO)
from abc import ABC, abstractmethod
from functools import wraps

def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name} is starting task: {func.__name__}...")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name} finished task: {func.__name__}")
        return result
    return wrapper

class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        message = f"{name} needs {required}% battery for this task, but only has {available}%."
        super().__init__(message)
        self.name = name
        self.required = required
        self.available = available


class Robot(ABC):
    manufacturer = "Ritwal"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = 0
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

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(name=config["name"], battery=config.get("battery", 100))

    @abstractmethod
    def perform_task(self):
        pass

class CoffeeBlenderRobot(Robot):
    def __init__(self, name, battery=100, bean_supply=50):
        super().__init__(name, battery)
        self.bean_supply = bean_supply

    @log_action 
    def perform_task(self):
        cost = 20
        self.use_battery(cost)
        self.bean_supply -= 5
        return f"{self.name} brewed a coffee. Beans remaining: {self.bean_supply}."

class DispenserRobot(Robot):
    def __init__(self, name, battery=100, cup_supply=50):
        super().__init__(name, battery)
        self.cup_supply = cup_supply

    def perform_task(self):
        cost = 10
        self.use_battery(cost)
        self.cup_supply -= 1
        return f"{self.name} dispensed a cup. Cups remaining: {self.cup_supply}."

def fleet_report(robots):
    print("--- Fleet Report ---")
    for robot in robots:
        print(str(robot))

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"[{robot.name}] Current battery: {robot.battery}%")

if __name__ == "__main__":
    config = {"name": "Config-Bot", "battery": 30}
    blender_from_config = CoffeeBlenderRobot.from_config(config)
    print(str(blender_from_config))
    print(type(blender_from_config))