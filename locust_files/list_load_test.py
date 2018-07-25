from locust import HttpLocust, TaskSet, task

api_url = "{user}"

class UserBehavior(TaskSet):
    @task(1)
    def list(self):
        self.client.get("/api/zaboes/")



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000