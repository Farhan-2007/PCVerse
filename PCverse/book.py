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
        psu = Category(name="Power Supply")
        cabinet = Category(name="Cabinet")
        cooler = Category(name="CPU Cooler")
        monitor = Category(name="Monitor")
        keyboard = Category(name="Keyboard")
        mouse = Category(name="Mouse")

        db.session.add_all([
            cpu,
            gpu,
            motherboard,
            ram,
            ssd,
            psu,
            cabinet,
            cooler,
            monitor,
            keyboard,
            mouse
        ])
        db.session.commit()

# Products

        products = [

            # ================= CPUs =================

            Product(
                name="AMD Ryzen 5 7600",
                brand="AMD",
                description="6-Core, 12-Thread Desktop Processor with AM5 Socket.",
                price=21999,
                stock=20,
                image_file="ryzen7600.jpg",
                category_id=cpu.id
            ),

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
                image_file="inteli5k.jpg",
                category_id=cpu.id
            ),

            # ================= GPUs =================

            Product(
                name="NVIDIA GeForce RTX 4060",
                brand="NVIDIA",
                description="Excellent graphics card for 1080p and entry-level 1440p gaming.",
                price=31999,
                stock=14,
                image_file="rtx4060.jpg",
                category_id=gpu.id
            ),

            Product(
                name="NVIDIA GeForce RTX 5070",
                brand="NVIDIA",
                description="High-performance graphics card for gaming and content creation.",
                price=64999,
                stock=10,
                image_file="rtx5070.jpg",
                category_id=gpu.id
            ),

            Product(
                name="AMD Radeon RX 7800 XT",
                brand="AMD",
                description="Powerful GPU for high-refresh-rate 1440p gaming.",
                price=52999,
                stock=11,
                image_file="rx7800xt.jpg",
                category_id=gpu.id
            ),

            # ================= Motherboards =================

            Product(
                name="ASUS TUF Gaming B650-Plus WiFi",
                brand="ASUS",
                description="AM5 motherboard with DDR5 support and PCIe 5.0.",
                price=18999,
                stock=12,
                image_file="asusb650.jpg",
                category_id=motherboard.id
            ),

            Product(
                name="MSI MAG B650 Tomahawk WiFi",
                brand="MSI",
                description="Premium AM5 motherboard with WiFi 6E and DDR5 support.",
                price=20999,
                stock=10,
                image_file="msib650.jpg",
                category_id=motherboard.id
            ),

            # ================= RAM =================

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
                name="G.Skill Trident Z5 RGB 32GB",
                brand="G.Skill",
                description="High-speed DDR5 RGB Gaming Memory.",
                price=12499,
                stock=15,
                image_file="tridentz5.jpg",
                category_id=ram.id
            ),

            # ================= SSD =================

            Product(
                name="Samsung 990 Pro 1TB",
                brand="Samsung",
                description="PCIe Gen4 NVMe SSD with ultra-fast read/write speeds.",
                price=9999,
                stock=25,
                image_file="990pro.jpg",
                category_id=ssd.id
            ),

            Product(
                name="WD Black SN850X 1TB",
                brand="Western Digital",
                description="High-performance NVMe SSD for gaming and creators.",
                price=9699,
                stock=18,
                image_file="sn850x.jpg",
                category_id=ssd.id
            ),

            # ================= Power Supplies =================

            Product(
                name="Corsair RM750e",
                brand="Corsair",
                description="750W 80+ Gold Fully Modular Power Supply.",
                price=8999,
                stock=15,
                image_file="corsair_rm750e.jpg",
                category_id=psu.id
            ),

            Product(
                name="Cooler Master MWE 750 Gold V2",
                brand="Cooler Master",
                description="750W Fully Modular Gold Rated PSU.",
                price=8499,
                stock=14,
                image_file="coolermaster_mwe750.jpg",
                category_id=psu.id
            ),

            # ================= Cabinets =================

            Product(
                name="Corsair 4000D Airflow",
                brand="Corsair",
                description="High-airflow mid-tower ATX cabinet.",
                price=7499,
                stock=12,
                image_file="4000d.jpg",
                category_id=cabinet.id
            ),

            Product(
                name="NZXT H5 Flow",
                brand="NZXT",
                description="Compact airflow-focused gaming cabinet.",
                price=7999,
                stock=10,
                image_file="h5flow.jpg",
                category_id=cabinet.id
            ),

            # ================= CPU Coolers =================

            Product(
                name="DeepCool AK620",
                brand="DeepCool",
                description="Dual Tower High Performance Air CPU Cooler.",
                price=5499,
                stock=18,
                image_file="ak620.jpg",
                category_id=cooler.id
            ),

            Product(
                name="Cooler Master Hyper 212",
                brand="Cooler Master",
                description="Classic air cooler with excellent cooling performance.",
                price=3499,
                stock=20,
                image_file="hyper212.jpg",
                category_id=cooler.id
            ),

            # ================= Monitors =================

            Product(
                name="LG UltraGear 27GR75Q",
                brand="LG",
                description="27-inch QHD 165Hz Gaming Monitor.",
                price=24999,
                stock=8,
                image_file="lg75q.jpg",
                category_id=monitor.id
            ),

            Product(
                name="ASUS TUF Gaming VG27AQ",
                brand="ASUS",
                description="27-inch IPS 165Hz Gaming Monitor with G-Sync Compatible.",
                price=26999,
                stock=7,
                image_file="vg27aq.jpg",
                category_id=monitor.id
            )

        ]

        db.session.add_all(products)
        db.session.commit()

        print("PCVerse sample data inserted successfully!")

    else:
        print("Database already contains data.")