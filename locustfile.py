from locust import HttpUser, task, between

class web_user(HttpUser):
    wait_time = between(1, 2)

    @task
    def search_authors(self):
        self.client.get("/authors?q=Mark")