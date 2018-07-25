from locust import HttpLocust, TaskSet, task
import json
from locust.clients import HttpSession

class UserBehavior(TaskSet):
    @task(1)
    def detail(self):
        zabo = self.client.get("/api/zaboes/100/")
        image_url = json.loads(zabo.content)["posters"][0]["image"]
        session = HttpSession(base_url="")
        session.get(image_url)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000