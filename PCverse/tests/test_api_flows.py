import unittest

from app import create_app, db
from app.models import Build, BuildItem, Category, Product


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-only-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ["http://localhost:5173"]
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False


class ApiFlowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        specs = {
            "CPU": "Socket: AM5\nCores: 8\nBoost Clock: 5.0 GHz\nTDP: 105W",
            "Motherboard": "Socket: AM5\nRAM Type: DDR5\nPCIe Version: PCIe 4.0",
            "RAM": "Type: DDR5\nCapacity: 32 GB\nSpeed: 6000 MHz",
            "GPU": (
                "VRAM: 12 GB\nBoost Clock: 2.5 GHz\n"
                "Power Consumption: 250W\nLength: 300 mm\n"
                "Interface: PCIe 4.0 x16"
            ),
            "Power Supply": "Wattage: 850W",
            "CPU Cooler": "Socket Support: AM5",
            "Cabinet": "GPU Clearance: 350 mm",
            "SSD": "Capacity: 1 TB",
        }
        self.product_ids = {}
        self.bad_motherboard_id = None
        self.out_of_stock_id = None

        for name, specification in specs.items():
            category = Category(name=name)
            db.session.add(category)
            db.session.flush()
            product = Product(
                name=f"Test {name}",
                brand="TestBrand",
                description="In-memory test component",
                price=1000,
                stock=5,
                specification=specification,
                image_file="default_product.jpg",
                category_id=category.id,
            )
            db.session.add(product)
            db.session.flush()
            self.product_ids[name] = product.id

            if name == "CPU":
                out_of_stock = Product(
                    name="Out of stock CPU",
                    brand="TestBrand",
                    description="Unavailable test component",
                    price=1000,
                    stock=0,
                    specification=specification,
                    image_file="default_product.jpg",
                    category_id=category.id,
                )
                db.session.add(out_of_stock)
                db.session.flush()
                self.out_of_stock_id = out_of_stock.id

            if name == "Motherboard":
                incompatible = Product(
                    name="Incompatible motherboard",
                    brand="TestBrand",
                    description="In-memory test component",
                    price=1000,
                    stock=5,
                    specification=(
                        "Socket: LGA1700\nRAM Type: DDR5\n"
                        "PCIe Version: PCIe 4.0"
                    ),
                    image_file="default_product.jpg",
                    category_id=category.id,
                )
                db.session.add(incompatible)
                db.session.flush()
                self.bad_motherboard_id = incompatible.id

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def csrf_token(self):
        response = self.client.get(
            "/api/csrf-token",
            headers={"Origin": "http://localhost:5173"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Credentials"),
            "true",
        )
        return response.get_json()["csrf_token"]

    def sign_up(self, token, username="tester"):
        return self.client.post(
            "/api/signup",
            json={
                "username": username,
                "email": f"{username}@example.test",
                "password": "password123",
            },
            headers={"X-CSRF-Token": token},
        )

    def test_csrf_auth_ownership_and_build_crud(self):
        self.assertEqual(self.client.get("/api/builds").status_code, 401)
        token = self.csrf_token()
        self.assertEqual(
            self.client.post("/api/signup", json={"username": "no-token"}).status_code,
            400,
        )
        self.assertEqual(self.sign_up(token).status_code, 201)

        response = self.client.post(
            "/api/builds",
            json={"name": "Smoke build"},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(response.status_code, 201)
        build_id = response.get_json()["build"]["id"]

        add_url = (
            f"/api/builds/{build_id}/items/"
            f"{self.product_ids['CPU']}"
        )
        self.assertEqual(
            self.client.post(add_url, headers={"X-CSRF-Token": token}).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(add_url, headers={"X-CSRF-Token": token}).status_code,
            400,
        )
        detail = self.client.get(f"/api/builds/{build_id}").get_json()
        self.assertEqual(len(detail["items"]), 1)
        item_id = detail["items"][0]["id"]
        removed = self.client.delete(
            f"/api/builds/{build_id}/items/{item_id}",
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(removed.status_code, 200)
        self.assertEqual(
            len(self.client.get(f"/api/builds/{build_id}").get_json()["items"]),
            0,
        )

        self.client.post("/api/logout", headers={"X-CSRF-Token": token})
        self.assertEqual(self.sign_up(token, username="second").status_code, 201)
        self.assertEqual(self.client.get(f"/api/builds/{build_id}").status_code, 404)

    def test_incompatible_component_add_and_swap_are_rejected(self):
        token = self.csrf_token()
        self.assertEqual(self.sign_up(token).status_code, 201)
        response = self.client.post(
            "/api/builds",
            json={"name": "Compatibility test"},
            headers={"X-CSRF-Token": token},
        )
        build_id = response.get_json()["build"]["id"]

        out_of_stock = self.client.post(
            f"/api/builds/{build_id}/items/{self.out_of_stock_id}",
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(out_of_stock.status_code, 400)
        self.assertEqual(out_of_stock.get_json()["message"], "This component is out of stock.")

        for category in ("CPU", "Motherboard"):
            self.assertEqual(
                self.client.post(
                    f"/api/builds/{build_id}/items/{self.product_ids[category]}",
                    headers={"X-CSRF-Token": token},
                ).status_code,
                200,
            )

        rejected_add = self.client.post(
            f"/api/builds/{build_id}/items/{self.bad_motherboard_id}",
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(rejected_add.status_code, 400)
        detail = self.client.get(f"/api/builds/{build_id}").get_json()
        motherboard_item = next(
            item for item in detail["items"]
            if item["category"] == "Motherboard"
        )
        rejected_swap = self.client.post(
            (
                f"/api/builds/{build_id}/items/{motherboard_item['id']}"
                f"/swap/{self.bad_motherboard_id}"
            ),
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(rejected_swap.status_code, 400)

    def test_recommendation_and_atomic_build_creation(self):
        token = self.csrf_token()
        self.assertEqual(self.sign_up(token).status_code, 201)
        result = self.client.post(
            "/api/recommendation",
            json={"usage": "gaming", "budget": 100000},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(result.status_code, 200, result.get_json())
        self.assertEqual(len(result.get_json()["recommendations"]), 8)

        created = self.client.post(
            "/api/recommendation/build",
            json={"usage": "gaming", "budget": 100000},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(created.status_code, 201, created.get_json())
        build_id = created.get_json()["build"]["id"]
        build = self.client.get(f"/api/builds/{build_id}").get_json()
        self.assertEqual(len(build["items"]), 8)

        invalid = self.client.post(
            "/api/recommendation/build",
            json={"usage": "gaming", "budget": float("inf")},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(invalid.status_code, 400)

    def test_jinja_pages_and_forms_render(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertNotIn(b"Featured Components", home.data)
        self.assertNotIn(b"Test CPU", home.data)
        stylesheet = self.client.get("/static/css/product.css")
        self.assertEqual(stylesheet.status_code, 200)
        stylesheet.close()
        products_page = self.client.get("/products?search=Test")
        self.assertEqual(products_page.status_code, 200)
        self.assertIn(b"Test CPU", products_page.data)
        self.assertEqual(
            self.client.get(f"/product/{self.product_ids['CPU']}").status_code,
            200,
        )
        with self.app.app_context():
            cpu_category = Category.query.filter_by(name="CPU").first()
            category_id = cpu_category.id
        self.assertEqual(self.client.get(f"/category/{category_id}").status_code, 200)
        self.assertEqual(self.client.get("/recommendation").status_code, 200)
        self.assertEqual(self.client.get("/login").status_code, 200)
        self.assertEqual(self.client.get("/signup").status_code, 200)

        token = self.csrf_token()
        self.assertEqual(self.sign_up(token).status_code, 201)
        self.assertEqual(self.client.get("/my-builds").status_code, 200)
        create = self.client.post(
            "/create-build",
            data={"name": "Template build", "csrf_token": token},
        )
        self.assertEqual(create.status_code, 302)
        with self.app.app_context():
            build_id = Build.query.filter_by(name="Template build").one().id
        add = self.client.post(
            f"/build/{build_id}/add/{self.product_ids['CPU']}",
            data={"csrf_token": token},
        )
        self.assertEqual(add.status_code, 302)
        self.assertEqual(self.client.get(f"/build/{build_id}").status_code, 200)
        with self.app.app_context():
            item_id = BuildItem.query.filter_by(build_id=build_id).one().id
        self.assertEqual(
            self.client.get(f"/build/{build_id}/swap/{item_id}").status_code,
            200,
        )


if __name__ == "__main__":
    unittest.main()
