from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():

    product = Product.query.filter_by(name = "AMD Ryzen 5 7600").first()

    if product:
                product.specification = """Socket: AM5
Cores: 6
Threads: 12
Base Clock: 3.8 GHz
Boost Clock: 5.1 GHz
TDP: 65W"""
                
    product = Product.query.filter_by(name = "AMD Ryzen 7 7700X").first()

    if product :
                
                product.specification = """Socket: AM5
Cores: 8
Threads: 16
Base Clock: 4.5 GHz
Boost Clock: 5.4 GHz
TDP: 105W"""
                
    product = Product.query.filter_by(name = "Intel Core i5-14600K").first()

    if product :
                
                product.specification = """Socket: LGA1700
Cores: 14
Threads: 20
Base Clock: 3.5 GHz
Boost Clock: 5.3 GHz
TDP: 125W"""

    product = Product.query.filter_by(name = "NVIDIA GeForce RTX 4060").first()

    if product :
                product.specification = """VRAM: 8 GB
Memory Type: GDDR6
Boost Clock: 2.46 GHz
Power Consumption: 115W
Interface: PCIe 4.0"""
                
    product = Product.query.filter_by(name = "NVIDIA GeForce RTX 5070").first()

    if product :
                product.specification = """VRAM: 12 GB
Memory Type: GDDR7
Boost Clock: 2.51 GHz
Power Consumption: 250W
Interface: PCIe 5.0"""
                
    
    product = Product.query.filter_by(name = "AMD Radeon RX 7800 XT").first()

    if product :
                product.specification = """VRAM: 16 GB
Memory Type: GDDR6
Boost Clock: 2.43 GHz
Power Consumption: 263W
Interface: PCIe 4.0"""


# ================= MOTHERBOARDS =================

    product = Product.query.filter_by(name="ASUS TUF Gaming B650-Plus WiFi").first()

    if product:
                product.specification = """Socket: AM5
Chipset: B650
RAM Type: DDR5
Maximum RAM: 128 GB
RAM Slots: 4
Form Factor: ATX"""


    product = Product.query.filter_by(name="MSI MAG B650 Tomahawk WiFi").first()

    if product:
                product.specification = """Socket: AM5
Chipset: B650
RAM Type: DDR5
Maximum RAM: 128 GB
RAM Slots: 4
Form Factor: ATX"""

# ================= RAM =================

    product = Product.query.filter_by(name="Corsair Vengeance DDR5 32GB").first()

    if product:
                product.specification = """Capacity: 32 GB
Type: DDR5
Speed: 6000 MHz
Modules: 2 x 16 GB
Voltage: 1.35V"""


    product = Product.query.filter_by(name="G.Skill Trident Z5 RGB 32GB").first()

    if product:
                product.specification = """Capacity: 32 GB
Type: DDR5
Speed: 6000 MHz
Modules: 2 x 16 GB
Voltage: 1.35V"""

# ================= SSD =================

    product = Product.query.filter_by(name="Samsung 990 Pro 1TB").first()

    if product:
                product.specification = """Capacity: 1 TB
Type: NVMe SSD
Interface: PCIe 4.0
Read Speed: 7450 MB/s
Write Speed: 6900 MB/s"""


    product = Product.query.filter_by(name="WD Black SN850X 1TB").first()

    if product:
                product.specification = """Capacity: 1 TB
Type: NVMe SSD
Interface: PCIe 4.0
Read Speed: 7300 MB/s
Write Speed: 6300 MB/s"""

# ================= POWER SUPPLIES =================

    product = Product.query.filter_by(name="Corsair RM750e").first()

    if product:
                product.specification = """Wattage: 750W
Efficiency: 80+ Gold
Modular: Fully Modular
Form Factor: ATX"""


    product = Product.query.filter_by(name="Cooler Master MWE 750 Gold V2").first()

    if product:
                product.specification = """Wattage: 750W
Efficiency: 80+ Gold
Modular: Fully Modular
Form Factor: ATX"""

# ================= CABINETS =================

    product = Product.query.filter_by(name="Corsair 4000D Airflow").first()

    if product:
                product.specification = """Form Factor: Mid Tower
Motherboard Support: ATX
GPU Clearance: 360 mm
CPU Cooler Clearance: 170 mm
Front Radiator Support: 360 mm
Side Panel: Tempered Glass"""


    product = Product.query.filter_by(name="NZXT H5 Flow").first()

    if product:
                product.specification = """Form Factor: Mid Tower
Motherboard Support: ATX
GPU Clearance: 365 mm
CPU Cooler Clearance: 165 mm
Front Radiator Support: 240 mm
Side Panel: Tempered Glass"""

# ================= CPU COOLERS =================

    product = Product.query.filter_by(name="DeepCool AK620").first()

    if product:
                product.specification = """Type: Dual Tower Air Cooler
Socket Support: AM5, AM4, LGA1700, LGA1200
Fan Size: 120 mm
Number of Fans: 2
TDP: 260W
Height: 160 mm"""


    product = Product.query.filter_by(name="Cooler Master Hyper 212").first()

    if product:
                product.specification = """Type: Tower Air Cooler
Socket Support: AM5, AM4, LGA1700
Fan Size: 120 mm
Number of Fans: 1
TDP: 180W
Height: 159 mm"""

# ================= MONITORS =================

    product = Product.query.filter_by(name="LG UltraGear 27GR75Q").first()

    if product:
                product.specification = """Screen Size: 27 inch
Resolution: 2560 x 1440
Panel Type: IPS
Refresh Rate: 165 Hz
Response Time: 1 ms
Adaptive Sync: FreeSync
Ports: HDMI, DisplayPort"""


    product = Product.query.filter_by(name="ASUS TUF Gaming VG27AQ").first()

    if product:
                product.specification = """Screen Size: 27 inch
Resolution: 2560 x 1440
Panel Type: IPS
Refresh Rate: 165 Hz
Response Time: 1 ms
Adaptive Sync: G-SYNC Compatible
Ports: HDMI, DisplayPort"""

# ================= KEYBOARDS =================

    product = Product.query.filter_by(name="Redragon K552 Kumara").first()

    if product:
                product.specification = """Type: Mechanical Gaming Keyboard
Switch Type: Red
RGB Lighting: Yes
Connectivity: USB
Key Travel: 2.0 mm"""

    product = Product.query.filter_by(name="Logitech G Pro X Keyboard").first()

    if product:
                product.specification = """Type: Mechanical Gaming Keyboard
Switch Type: Brown
RGB Lighting: Yes
Connectivity: USB
Key Travel: 2.0 mm"""

# ================= MOUSE =================
    product = Product.query.filter_by(name="Logitech G502 HERO").first()

    if product:
                product.specification = """Type: Gaming Mouse
Sensor: HERO
DPI: 25000
Buttons: 8
Connectivity: USB"""

    product = Product.query.filter_by(name="Razer DeathAdder V2").first()

    if product:
                product.specification = """Type: Gaming Mouse
Sensor: OPM
DPI: 16000
Buttons: 8
Connectivity: USB"""
    db.session.commit()

    print("ALL specifications updated successfully!")