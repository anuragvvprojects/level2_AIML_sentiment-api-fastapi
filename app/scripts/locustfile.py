from locust import HttpUser, task, between
class User(HttpUser):
    wait_time = between(1, 2)
    @task
    def predict(self):
        self.client.post("/predict", json={"text": "I love this!"})
