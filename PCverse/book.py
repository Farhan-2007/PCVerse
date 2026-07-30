from app import create_app, db
from app.models import Category, Product

app = create_app()

with app.app_context():

    if Category.query.count() == 0:

        # Categories

        cpu = Category(name="CPU")
        gpu = Category(name="GPU")
        motherboard = Category(name="Motherboard")
        ram = Category(name="RAM")
        ssd = Category(name="SSD")
        psu = Category(name="PSU")

        db.session.add_all([
            cpu,
            gpu,
            motherboard,
            ram,
            ssd,
            psu
        ])

        db.session.commit()

        # Products

        products = [

            Product(
                name="AMD Ryzen 7 7700X",
                brand="AMD",
                description="8-Core, 16-Thread Desktop Processor with AM5 Socket.",
                price=29999,
                stock=15,
                image_file="ryzen7700x.jpg",
                category_id=cpu.id
            ),

            Product(
                name="Intel Core i5-14600K",
                brand="Intel",
                description="14-Core Desktop Processor for Gaming and Productivity.",
                price=28999,
                stock=18,
                image_file="i5_14600k.jpg",
                category_id=cpu.id
            ),

            Product(
                name="NVIDIA GeForce RTX 5070",
                brand="NVIDIA",
                description="Powerful graphics card built for high-end gaming and content creation.",
                price=64999,
                stock=10,
                image_file="rtx5070.jpg",
                category_id=gpu.id
            ),

            Product(
                name="ASUS TUF Gaming B650-Plus WiFi",
                brand="ASUS",
                description="AM5 motherboard with DDR5 support and PCIe 5.0.",
                price=18999,
                stock=12,
                image_file="b650plus.jpg",
                category_id=motherboard.id
            ),

            Product(
                name="Corsair Vengeance DDR5 32GB",
                brand="Corsair",
                description="32GB (2×16GB) DDR5 6000MHz Desktop Memory Kit.",
                price=10999,
                stock=20,
                image_file="corsair_ddr5.jpg",
                category_id=ram.id
            ),

            Product(
                name="Samsung 990 Pro 1TB",
                brand="Samsung",
                description="PCIe Gen4 NVMe M.2 SSD delivering ultra-fast read and write speeds.",
                price=9999,
                stock=25,
                image_file="990pro.jpg",
                category_id=ssd.id
            ),

            Product(
                name="Corsair RM750e",
                brand="Corsair",
                description="750W 80+ Gold Fully Modular Power Supply.",
                price=8999,
                stock=15,
                image_file="rm750e.jpg",
                category_id=psu.id
            )

        ]

        db.session.add_all(products)
        db.session.commit()

        print("PCVerse sample data inserted successfully!")

    else:
        print("Database already contains data.")