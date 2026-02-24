from locust import HttpUser, task, between
import random

class WebUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post(
            "/books",
            data={
                "title": "Initial Book",
                "author": "Locust Author",
                "publisher": "Locust Publisher",
                "first_publish_year": 2026,
            }
        )
        if response.status_code == 200 or response.status_code == 201:
            self.book_id = response.json()["id"]
        else:
            self.book_id = None

    @task
    def search_authors(self):
        self.client.get("/authors", params={"q": "Mark Lutz"})

    @task
    def search_books(self):
        self.client.get("/books", params={"q": "python"})

    @task
    def delete_book(self):
        if hasattr(self, "book_id") and self.book_id is not None:
            self.client.delete(f"/books/{self.book_id}")
            response = self.client.post(
                "/books",
                data={
                    "title": "New Book",
                    "author": "Locust Author",
                    "publisher": "Locust Publisher",
                    "first_publish_year": 2026,
                }
            )
            if response.status_code == 200 or response.status_code == 201:
                self.book_id = response.json()["id"]

    @task
    def add_book(self):
        response = self.client.post(
            "/books",
            data={
                "title": f"Book {random.randint(1,1000)}",
                "author": "Hadi",
                "publisher": "Science",
                "first_publish_year": random.randint(1950, 2026),
            },
        )
        if response.status_code == 200 or response.status_code == 201:
            self.book_id = response.json()["id"]

    @task
    def update_fully_book(self):
        if hasattr(self, "book_id") and self.book_id is not None and self.book_id < 999:
            self.client.put(
                f"/books/{self.book_id}",
                data={
                    "title": f"Updated Book {random.randint(1,1000)}",
                    "author": "Updated Author",
                    "publisher": "Updated Publisher",
                    "first_publish_year": 2000,
                },
            )

    @task
    def update_book_part(self):
        if hasattr(self, "book_id") and self.book_id is not None and self.book_id < 999:
            self.client.patch(
                f"/books/{self.book_id}",
                data={
                    "title": f"Patch Title {random.randint(1,1000)}",
                },
            )