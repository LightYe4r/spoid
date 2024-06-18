from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cpu, Memory, Cooler, Case, Power, MainBoard, Gpu, Storage, Price
from .serializers import CpuSerializer, MemorySerializer, CoolerSerializer, CaseSerializer, PowerSerializer, MainBoardSerializer, GpuSerializer, StorageSerializer, PriceSerializer
import random
from datetime import datetime

class InsertDummyDataView(APIView):
    def post(self, request):
        try:
            # 각 부품별 더미 데이터를 20개씩 생성하고 Price 데이터를 3개씩 추가
            shops = ["다나와", "샵다나와", "컴퓨존"]
            today = datetime.today().date()

            # CPU 더미 데이터
            cpu_data_list = [
                {
                    "cpu_id": "CPU#"+f"Intel Core i9-{i}#"+"Intel",
                    "model": f"Intel Core i9-{i}",
                    "company": "Intel",
                    "process": "10nm",
                    "socket": "LGA1200",
                    "core": random.randint(4, 16),
                    "thread": random.randint(8, 32),
                    "clock": round(random.uniform(2.5, 3.8), 2),
                    "boost": round(random.uniform(4.0, 5.2), 2),
                    "memory": "DDR4-2933",
                    "l3_cache": "16MB",
                    "graphic": "Intel UHD Graphics 630",
                    "gpu_clock": "350 MHz",
                    "image_url": f"http://example.com/cpu{i}.jpg"
                } for i in range(20)
            ]

            # Memory 더미 데이터
            memory_data_list = [
                {
                    "memory_id": "Memory#"+f"Corsair Vengeance LPX-{i}#Corsair",
                    "model": f"Corsair Vengeance LPX-{i}",
                    "company": "Corsair",
                    "use_case": "Gaming",
                    "ram_timing": "16-18-18-36",
                    "xmp": True,
                    "rgb": bool(random.getrandbits(1)),
                    "image_url": f"http://example.com/memory{i}.jpg"
                } for i in range(20)
            ]

            # Cooler 더미 데이터
            cooler_data_list = [
                {
                    "cooler_id": "Cooler#"+f"Cooler Master Hyper 212-{i}#Cooler Master",
                    "model": f"Cooler Master Hyper 212-{i}",
                    "company": "Cooler Master",
                    "size": "120mm",
                    "rpm": random.randint(1200, 2000),
                    "led": bool(random.getrandbits(1)),
                    "noise": f"{random.randint(20, 35)} dBA",
                    "image_url": f"http://example.com/cooler{i}.jpg"
                } for i in range(20)
            ]

            # Case 더미 데이터
            case_data_list = [
                {
                    "case_id": "Case#"+f"NZXT H510-{i}#NZXT",
                    "model": f"NZXT H510-{i}",
                    "company": "NZXT",
                    "size": "Mid Tower",
                    "storage": "2.5\" x 2, 3.5\" x 2",
                    "cooling_fan": "4 x 120mm",
                    "ladiator": "240mm",
                    "cpu_cooler": "165mm",
                    "power_size": "ATX",
                    "gpu": "381mm",
                    "chassis": "Steel",
                    "cpu_temp": round(random.uniform(45.0, 60.0), 1),
                    "gpu_temp": round(random.uniform(50.0, 70.0), 1),
                    "image_url": f"http://example.com/case{i}.jpg"
                } for i in range(20)
            ]

            # Power 더미 데이터
            power_data_list = [
                {
                    "power_id": "Power#"+f"EVGA 600W-{i}#EVGA",
                    "model": f"EVGA 600W-{i}",
                    "company": "EVGA",
                    "maximum_output": 600,
                    "eighty_plus": "Bronze",
                    "modular": bool(random.getrandbits(1)),
                    "form_factor": "ATX",
                    "cooling_fan": "120mm",
                    "bearing": "Sleeve",
                    "warranty": 5,
                    "full_load": round(random.uniform(80.0, 90.0), 1),
                    "voltage_drop": round(random.uniform(2.0, 4.0), 1),
                    "max_rpm": random.randint(1500, 2000),
                    "image_url": f"http://example.com/power{i}.jpg"
                } for i in range(20)
            ]
            # MainBoard 더미 데이터
            mainboard_data_list = [
                {
                    "mainboard_id": "MainBoard#"+f"ASUS ROG STRIX-{i}#ASUS",
                    "model": f"ASUS ROG STRIX-{i}",
                    "company": "ASUS",
                    "use_case": "Gaming",
                    "socket": "AM4",
                    "chipset": "X570",
                    "form_factor": "ATX",
                    "memory": "DDR4",
                    "dimm": 4,
                    "m_2": 2,
                    "sata": 6,
                    "vrm": "14 Phase",
                    "power_limit": "300W",
                    "temp": round(random.uniform(50.0, 70.0), 1),
                    "image_url": f"http://example.com/mainboard{i}.jpg"
                } for i in range(20)
            ]
            # GPU 더미 데이터
            gpu_data_list = [
                {
                    "gpu_id": "GPU#"+f"NVIDIA GeForce RTX 3080-{i}#NVIDIA",
                    "model": f"NVIDIA GeForce RTX 3080-{i}",
                    "company": "NVIDIA",
                    "manufacturer": "NVIDIA",
                    "boost_clock": round(random.uniform(1.5, 1.9), 2),
                    "memory": "10GB GDDR6X",
                    "length": random.randint(250, 300),
                    "basic_power": random.randint(250, 350),
                    "maximum_power": random.randint(300, 400),
                    "vrm": "8 Phase",
                    "core_degree": round(random.uniform(60.0, 80.0), 1),
                    "noise": f"{random.randint(30, 40)} dBA",
                    "image_url": f"http://example.com/gpu{i}.jpg"
                } for i in range(20)
            ]

            # Storage 더미 데이터
            storage_data_list = [
                {
                    "storage_id": "Storage#"+f"Samsung 970 EVO-{i}#Samsung",
                    "model": f"Samsung 970 EVO-{i}",
                    "company": "Samsung",
                    "capacity": "1TB",
                    "nand": "V-NAND",
                    "interface": "PCIe Gen 3.0 x4",
                    "form_factor": "M.2",
                    "dram": "Yes",
                    "read_performance": random.randint(3000, 3500),
                    "write_performance": random.randint(3000, 3300),
                    "four_k_read": random.randint(400, 600),
                    "four_k_write": random.randint(400, 600),
                    "persistent_write": random.randint(200, 400),
                    "maximum_temp": round(random.uniform(60.0, 80.0), 1),
                    "image_url": f"http://example.com/storage{i}.jpg"
                } for i in range(20)
            ]

            # 데이터베이스에 더미 데이터 삽입 및 Price 데이터 생성
            for cpu_data in cpu_data_list:
                cpu_serializer = CpuSerializer(data=cpu_data)
                if cpu_serializer.is_valid():
                    cpu = cpu_serializer.save()
                    for shop in shops:
                        price_data = {
                            "cpu": cpu.cpu_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(300, 700), 2),
                            "url": "http://example.com/cpu_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("CPU data inserted successfully!")
            for memory_data in memory_data_list:
                memory_serializer = MemorySerializer(data=memory_data)
                if memory_serializer.is_valid():
                    memory = memory_serializer.save()
                    for shop in shops:
                        price_data = {
                            "memory": memory.memory_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(100, 200), 2),
                            "url": "http://example.com/memory_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Memory data inserted successfully!")
            for cooler_data in cooler_data_list:
                cooler_serializer = CoolerSerializer(data=cooler_data)
                if cooler_serializer.is_valid():
                    cooler = cooler_serializer.save()
                    for shop in shops:
                        price_data = {
                            "cooler": cooler.cooler_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(30, 70), 2),
                            "url": "http://example.com/cooler_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Cooler data inserted successfully!")
            for case_data in case_data_list:
                case_serializer = CaseSerializer(data=case_data)
                if case_serializer.is_valid():
                    case = case_serializer.save()
                    for shop in shops:
                        price_data = {
                            "case": case.case_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(70, 150), 2),
                            "url": "http://example.com/case_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Case data inserted successfully!")
            for power_data in power_data_list:
                power_serializer = PowerSerializer(data=power_data)
                if power_serializer.is_valid():
                    power = power_serializer.save()
                    for shop in shops:
                        price_data = {
                            "power": power.power_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(50, 120), 2),
                            "url": "http://example.com/power_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Power data inserted successfully!")
            for mainboard_data in mainboard_data_list:
                mainboard_serializer = MainBoardSerializer(data=mainboard_data)
                if mainboard_serializer.is_valid():
                    mainboard = mainboard_serializer.save()
                    for shop in shops:
                        price_data = {
                            "mainboard": mainboard.mainboard_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(100, 250), 2),
                            "url": "http://example.com/mainboard_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Mainboard data inserted successfully!")
            for gpu_data in gpu_data_list:
                gpu_serializer = GpuSerializer(data=gpu_data)
                if gpu_serializer.is_valid():
                    gpu = gpu_serializer.save()
                    for shop in shops:
                        price_data = {
                            "gpu": gpu.gpu_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(400, 800), 2),
                            "url": "http://example.com/gpu_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("GPU data inserted successfully!")
            for storage_data in storage_data_list:
                storage_serializer = StorageSerializer(data=storage_data)
                if storage_serializer.is_valid():
                    storage = storage_serializer.save()
                    for shop in shops:
                        price_data = {
                            "storage": storage.storage_id,
                            "date": today,
                            "shop": shop,
                            "price": round(random.uniform(100, 300), 2),
                            "url": "http://example.com/storage_price"
                        }
                        price_serializer = PriceSerializer(data=price_data)
                        if price_serializer.is_valid():
                            price_serializer.save()
            print("Storage data inserted successfully!")
            return Response({"message": "20 dummy data items inserted successfully for each component with prices!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ComponentListView(APIView):
    def post(self, request):
        data = request.data
        try:
            # 각 부품별 조회 시작 인덱스
            cpu_index = int(data.get("cpu_index"))
            memory_index = int(data.get("memory_index"))
            cooler_index = int(data.get("cooler_index"))
            case_index = int(data.get("case_index"))
            power_index = int(data.get("power_index"))
            mainboard_index = int(data.get("mainboard_index"))
            gpu_index = int(data.get("gpu_index"))
            storage_index = int(data.get("storage_index"))
            
            # 각 부품별 전체 데이터 10개씩 조회
            cpu_list = Cpu.objects.all()[cpu_index:cpu_index+10]
            memory_list = Memory.objects.all()[memory_index:memory_index+10]
            cooler_list = Cooler.objects.all()[cooler_index:cooler_index+10]
            case_list = Case.objects.all()[case_index:case_index+10]
            power_list = Power.objects.all()[power_index:power_index+10]
            mainboard_list = MainBoard.objects.all()[mainboard_index:mainboard_index+10]
            gpu_list = Gpu.objects.all()[gpu_index:gpu_index+10]
            storage_list = Storage.objects.all()[storage_index:storage_index+10]
            

            cpu_serializer = CpuSerializer(cpu_list, many=True)
            memory_serializer = MemorySerializer(memory_list, many=True)
            cooler_serializer = CoolerSerializer(cooler_list, many=True)
            case_serializer = CaseSerializer(case_list, many=True)
            power_serializer = PowerSerializer(power_list, many=True)
            mainboard_serializer = MainBoardSerializer(mainboard_list, many=True)
            gpu_serializer = GpuSerializer(gpu_list, many=True)
            storage_serializer = StorageSerializer(storage_list, many=True)

            # 각 부품별 데이터의 price 정보를 조회
            for i in range(len(cpu_list)):
                price = Price.objects.filter(cpu=cpu_list[i]).first()
                price_serializer = PriceSerializer(price)
                cpu_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(memory_list)):
                price = Price.objects.filter(memory=memory_list[i]).first()
                price_serializer = PriceSerializer(price)
                memory_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(cooler_list)):
                price = Price.objects.filter(cooler=cooler_list[i]).first()
                price_serializer = PriceSerializer(price)
                cooler_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(case_list)):
                price = Price.objects.filter(case=case_list[i]).first()
                price_serializer = PriceSerializer(price)
                case_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(power_list)):
                price = Price.objects.filter(power=power_list[i]).first()
                price_serializer = PriceSerializer(price)
                power_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(mainboard_list)):
                price = Price.objects.filter(mainboard=mainboard_list[i]).first()
                price_serializer = PriceSerializer(price)
                mainboard_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(gpu_list)):
                price = Price.objects.filter(gpu=gpu_list[i]).first()
                price_serializer = PriceSerializer(price)
                gpu_serializer.data[i]["price"] = price_serializer.data
                
            for i in range(len(storage_list)):
                price = Price.objects.filter(storage=storage_list[i]).first()
                price_serializer = PriceSerializer(price)
                storage_serializer.data[i]["price"] = price_serializer.data
            
            return Response({
                "cpu": cpu_serializer.data,
                "memory": memory_serializer.data,
                "cooler": cooler_serializer.data,
                "case": case_serializer.data,
                "power": power_serializer.data,
                "mainboard": mainboard_serializer.data,
                "gpu": gpu_serializer.data,
                "storage": storage_serializer.data,
                "price": price_serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
