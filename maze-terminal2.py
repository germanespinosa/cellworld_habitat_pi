from experiment import Experiment
from pi_service import PiService
from cellworld_experiment_service import ExperimentClient

client = ExperimentClient()
experiment = Experiment(client)
service = PiService(experiment,client)

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


