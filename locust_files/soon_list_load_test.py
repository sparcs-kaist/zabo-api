from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    @task(1)
    def detail(self):
        zabo = self.client.get("/api/zaboes/soon/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000