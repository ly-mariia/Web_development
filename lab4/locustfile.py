from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        self.token = "test-token"  # Assuming the token exists in the database
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def get_items(self):
        self.client.get("/items/")

    @task(2)
    def get_cart(self):
        self.client.get("/cart_items_sorted/?sort_by=name&order=asc")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
