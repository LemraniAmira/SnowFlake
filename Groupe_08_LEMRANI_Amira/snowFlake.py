import time
import threading

class SnowflakeIDGenerator:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.max_sequence = 4095

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_next_millisecond(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self):
        timestamp = self._current_timestamp()

        if timestamp == self.last_timestamp:
            self.sequence += 1
            if self.sequence > self.max_sequence:
                timestamp = self._wait_next_millisecond(self.last_timestamp)
                self.sequence = 0
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        snowflake_id = (
            (timestamp << 22) |
            (self.machine_id << 12) |
            self.sequence
        )
        return snowflake_id


class Machine(threading.Thread):
    def __init__(self, machine_id, count):
        super().__init__()
        self.generator = SnowflakeIDGenerator(machine_id)
        self.count = count

    def run(self):
        print(f"\nMachine {self.generator.machine_id} demarre...")
        for _ in range(self.count):
            snowflake_id = self.generator.generate_id()
            print(f"Machine {self.generator.machine_id} -> ID : {snowflake_id} \n")
            time.sleep(0.01)


if __name__ == "__main__":
    print("=== Simulation Snowflake ID Generator ===")

    machine1 = Machine(machine_id=1, count=5)
    machine2 = Machine(machine_id=2, count=5)

    machine1.start()
    machine2.start()

    machine1.join()
    machine2.join()

    print("\n=== Fin de la simulation ===")