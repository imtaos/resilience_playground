from locust import HttpUser, task

class BlogTest(HttpUser):

    @task
    def test_post_blog(self):
        payload = {
            "title": "Test Blog",
            "content": "Test Content",
            "author": "Test Author"
        }
        self.client.post("/post_blog",json=payload)

    # @task
    def test_get_blog(self):
        self.client.get("/get_blog/1")
