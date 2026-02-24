from locust import HttpUser, task, between


class WebUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def search_authors(self):
        self.client.get("/authors", params={"q": "Mark Lutz"})

    @task
    def search_books(self):
        self.client.get("/books", params={"q": "python"})

    @task
    def delete_book(self):
        book_id = 1010
        self.client.delete(f"/books/{book_id}")

    @task
    def add_book(self):
        self.client.post(
            "/books",
            json={
                "title": "Math",
                "author": "Hadi",
                "publisher": "science",
                "first_publish_year": 2000,
            },
        )

    @task
    def update_fully_book(self):
        book_id = 1020
        self.client.put(
            f"/books/{book_id}",
            json={
                "title": "c++",
                "author": "Naser",
                "publisher": "science",
                "first_publish_year": 1990,
            },
        )

    @task
    def update_book_part(self):
        book_id = 1020
        self.client.patch(
            f"/books/{book_id}",
            json={
                "title": "c++",
                "author": "Naser",
            },
        )
