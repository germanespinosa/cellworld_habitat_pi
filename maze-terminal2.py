import doors as door
import feeder
from experiment import Experiment
import json
from time import sleep
from pi_service import PiService
from cellworld_experiment_service import ExperimentClient
from json_cpp import JsonObject, JsonList
from os import path
from _thread import start_new_thread

client = ExperimentClient()
experiment = Experiment(client)
service = PiService(experiment,client)

# response = service.test_door(TestDoorResponse(1,3))
# print(response)
# response = service.status('bla')
# print(response)
# print(response.door_state)
# print(response.door_state[0])
# response = service.give_reward(1)
# print(response)

client.on_episode_started = experiment.episode_started
#client.on_experiment_finished = experiment.experiment_finished
client.on_experiment_started = experiment.experiment_started
client.on_episode_finished = experiment.episode_finished
print("connecting to client")
client.connect("192.168.137.41")
print("client connected")
client.subscribe()
print("client subscribed\n-------------------------")

print('starting server')
service.start()
print("service running\n-------------------------")
service.join()

while client.connection.state == Connection.State.Open:
    #print('waiting for response')
    while client.router.routing_count < 1 and client.connection.state == Connection.State.Open:
        pass
    #print(client.router.routing_count)
    client.router.routing_count = 0
    pass


