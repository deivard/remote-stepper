from machine import Pin
import time


class StepperMotor:
    def __init__(self, pins: list[int], steps_per_revolution: int = 24) -> None:
        self.__pins = [Pin(p, Pin.OUT) for p in pins]
        self.__cycles = [
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1],
            [1,0,0,1]
        ]

        self.__steps_per_revolution = steps_per_revolution
        self.__current_cycle_index = 0
        self.__step_angle = 360 / self.__steps_per_revolution
        self.__min_sleep_time = 0.012
        self.__max_sleep_time = 0.3
        self.__sleep_delta = self.__max_sleep_time - self.__min_sleep_time
        self.speed = 1

    def __set_pins(self, values):
        for pin, value in zip(self.__pins, values):
            pin.value(value)

    def __increment_cycle_index(self, value):
        self.__current_cycle_index = ((self.__current_cycle_index + value)
                                    % len(self.__cycles))

    def step(self, steps):
        increment = 1 if steps > 0 else -1
        for _ in range(abs(steps)):
            self.__increment_cycle_index(increment)
            self.__set_pins(self.__cycles[self.__current_cycle_index])
            time.sleep(self.__max_sleep_time - (self.speed * self.__sleep_delta))
    
    def step_angle(self, angle: int):
        steps = int(angle / self.__step_angle)
        self.step(steps)

    def idle(self):
        self.__set_pins([0,0,0,0])
