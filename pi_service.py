from tcp_messages import MessageServer, Message
import socket
from pi_messages import *
from _thread import start_new_thread

class PiService(MessageServer):
    def __init__(self,experiment,client):
        MessageServer.__init__(self)
        self.pi_name = socket.gethostname()
        self.experiment = experiment
        self.client = client
        self.router.add_route("open_door", self.open_door, int)
        self.router.add_route("close_door", self.close_door, int)
        self.router.add_route("calibrate_door", self.calibrate_door, int)
        self.router.add_route("save_calibration", self.save_calibration)
        self.router.add_route("give_reward", self.give_reward, int)
        self.router.add_route("enable_feeder", self.enable_feeder, int)
        self.router.add_route("feeder_reached", self.feeder_reached, int)
        self.router.add_route("test_feeder", self.test_feeder, TestFeederResponse)
        self.router.add_route("test_door", self.test_door, TestDoorResponse)
        self.router.add_route("status", self.status)
        self.allow_subscription = True

    def start(self):
        return MessageServer.start(self, PiService.port())

    def open_door(self, door_num) -> str:
        print(f"opening {door_num}")
        self.door_thread = start_new_thread(self.experiment.doors.open_door, (door_num,))
        return f"opened door{door_num}"

    def close_door(self, door_num) -> str:
        print(f"closing {door_num}")
        self.door_thread = start_new_thread(self.experiment.doors.close_door, (door_num,))
        return f"closed door{door_num}"

    def test_door(self, parameters: TestDoorResponse) -> str:
        # include check to see if door exists
        print(f"testing door{parameters.door_num} {parameters.repetition} times")
        self.door_thread = start_new_thread(self.experiment.doors.test_door, (parameters.door_num, parameters.repetition))
        return f"tested door{parameters.door_num} {parameters.repetition} times"

    def calibrate_door(self, door_num) -> str:
        self.experiment.doors.calibrate_door(door_num)
        return f"door{door_num} calibration finished"

    def save_calibration(self, m) -> str:
        print("saving calibration")
        self.experiment.doors.save_calibration()
        return "door calibration saved"

    def give_reward(self, feeder_num) -> str:
        if feeder_num == self.experiment.feeder_number:
            print(f"feeding feeder{feeder_num}")
            self.experiment.feeders.feed()
            return f"feeding {feeder_num}"
        return f"feeder{feeder_num} not found"

    def enable_feeder(self, feeder_num) -> str:
        if feeder_num == self.experiment.feeder_number:
            print(f"Enabling feeder{feeder_num}")
            self.experiment.feeders.active = True
        return f"Enabled feeder{feeder_num}"
        
    def feeder_reached(self, feeder_num) -> str:
        if feeder_num == self.experiment.feeder_number:
            print(f"Activating feeder{feeder_num}")
            self.experiment.feeders.report_feeder(self.client, self.experiment)
        return f"Activating feeder{feeder_num}"

    def test_feeder(self, parameters: TestFeederResponse) -> str:
        # include check to see if door existss
        if parameters.feeder_num == self.experiment.feeder_number:
            print(parameters.feedtime)
            print(parameters.repetition)
            print(parameters.wait_time)
            self.feeder_thread = start_new_thread(self.experiment.feeders.test, (parameters.feedtime, parameters.repetition, parameters.wait_time))
        return f"water has been outputted"

    def status(self, m) -> StatusResponse:
        # include check to see if door exists
        #status_response(door1_state='open', door2_state='open', feeder_state='enabled')
        #print(response)
        ID = self.pi_name
        door_state = self.experiment.doors.status()
        if self.experiment.feeders.active == True:
            feeder_state = "enabled"
        else:
            feeder_state = "disabled"
        return StatusResponse(ID = ID, door_state = door_state, feeder_state=feeder_state)

    @staticmethod
    def port(ip: str = '') -> int:
        if socket.gethostname() == "maze1":
            port_num = 4610
        else:
            port_num = 4620
        print(f'port = {port_num}')
        return port_num