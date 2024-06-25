from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(1,2)
    
    # @task
    # def index(self):
    #     self.client.get("/regular/search?song=a")

    # @task
    # def index2(self):
    #     self.client.get("/regular/top-charts?date=2017-01-01&country=Argentina")
    
    @task
    def index3(self):
        self.client.get("/regular/song-details/1")