from rest_framework import serializers

class CpuDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Process = serializers.CharField()
    Socket = serializers.CharField()
    Core = serializers.CharField()
    Thread = serializers.CharField()
    Clock = serializers.CharField()
    Boost = serializers.CharField()
    Memory = serializers.CharField()
    L3Cache = serializers.CharField()
    Graphic = serializers.CharField()
    GpuClock = serializers.CharField()
    ImageURL = serializers.CharField()

class PcCaseDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Size = serializers.CharField()
    Storage = serializers.CharField()
    CoolingFan = serializers.CharField()
    Ladiator = serializers.CharField()
    CpuCooler = serializers.CharField()
    PowerSize = serializers.CharField()
    Gpu = serializers.CharField()
    Chassis = serializers.CharField()
    CpuTemp = serializers.CharField()
    GpuTemp = serializers.CharField()
    ImageURL = serializers.CharField()

class ComponentAlarmDataSerializer(serializers.Serializer):
    ComponentAlarmID = serializers.CharField()
    ComponentID = serializers.CharField()
    FavoriteID = serializers.CharField()
    UserID = serializers.CharField()
    Type = serializers.CharField()
    Content = serializers.CharField()

class ComponentIDDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()

class CoolerDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Size = serializers.CharField()
    RPM = serializers.CharField()
    LED = serializers.CharField()
    Noise = serializers.CharField()
    Color = serializers.CharField()
    ImageURL = serializers.CharField()

class FavoriteDataSerializer(serializers.Serializer):
    FavoriteID = serializers.CharField()
    UserID = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()

class GpuDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Manufacturer = serializers.CharField()
    Company = serializers.CharField()
    GPU = serializers.CharField()
    BoostClock = serializers.CharField()
    Memory = serializers.CharField()
    Length = serializers.CharField()
    BasicPower = serializers.CharField()
    MaximumPower = serializers.CharField()
    VRM = serializers.CharField()
    CoreTemp = serializers.CharField()
    Noise = serializers.CharField()
    ImageURL = serializers.CharField()

class MainboardDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    UseCase = serializers.CharField()
    Socket = serializers.CharField()
    ChipSet = serializers.CharField()
    Form = serializers.CharField()
    Memory = serializers.CharField()
    DIMM = serializers.CharField()
    M_2 = serializers.CharField()
    SATA = serializers.CharField()
    VRM = serializers.CharField()
    PowerLimit = serializers.CharField()
    Temp = serializers.CharField()
    Color = serializers.CharField()
    ImageURL = serializers.CharField()

class MemoryDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Spec = serializers.CharField()
    UseCase = serializers.CharField()
    Speed = serializers.CharField()
    RamTiming = serializers.CharField()
    XMP = serializers.CharField()
    Color = serializers.CharField()
    RGB = serializers.CharField()
    ImageURL = serializers.CharField()

class OrdersDataSerializer(serializers.Serializer):
    OrderID = serializers.CharField()
    UserID = serializers.CharField()
    CPUID = serializers.CharField()
    CpuType = serializers.CharField()
    GPUID = serializers.CharField()
    GpuType = serializers.CharField()
    MemoryID = serializers.CharField()
    MemoryType = serializers.CharField()
    CoolerID = serializers.CharField()
    CoolerType = serializers.CharField()
    MainboardID = serializers.CharField()
    MainboardType = serializers.CharField()
    StorageID = serializers.CharField()
    StorageType = serializers.CharField()
    PcCaseID = serializers.CharField()
    PcCaseType = serializers.CharField()
    PowerID = serializers.CharField()
    PowerType = serializers.CharField()
    
class OrderAlarmDataSerializer(serializers.Serializer):
    OrderAlarmID = serializers.CharField()
    OrderID = serializers.CharField()
    UserID = serializers.CharField()
    Content = serializers.CharField()

class PowerDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    MaximumOutput = serializers.CharField()
    PLUS80 = serializers.CharField()
    Modular = serializers.CharField()
    FormFactor = serializers.CharField()
    CoolingFan = serializers.CharField()
    Bearing = serializers.CharField()
    Warranty = serializers.CharField()
    FullLoad = serializers.CharField()
    MaxRPM = serializers.CharField()
    ImageURL = serializers.CharField()

class PricdDataSerializer(serializers.Serializer):
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()

class StorageDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    NAND = serializers.CharField()
    Capacity = serializers.CharField()
    Interface = serializers.CharField()
    FormFactor = serializers.CharField()
    DRAM = serializers.CharField()
    ReadPerformance = serializers.CharField()
    WritePerformance = serializers.CharField()
    Read4K = serializers.CharField()
    Write4K = serializers.CharField()
    MaximumTemp = serializers.CharField()
    ImageURL = serializers.CharField()

class UserDataSerializer(serializers.Serializer):
    UserID = serializers.CharField()
    Email = serializers.CharField()
    Name = serializers.CharField()

class CpuPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Process = serializers.CharField()
    Socket = serializers.CharField()
    Core = serializers.CharField()
    Thread = serializers.CharField()
    Clock = serializers.CharField()
    Boost = serializers.CharField()
    Memory = serializers.CharField()
    L3Cache = serializers.CharField()
    Graphic = serializers.CharField()
    GpuClock = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()
    
class PcCasePriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Size = serializers.CharField()
    Storage = serializers.CharField()
    CoolingFan = serializers.CharField()
    Ladiator = serializers.CharField()
    CpuCooler = serializers.CharField()
    PowerSize = serializers.CharField()
    Gpu = serializers.CharField()
    Chassis = serializers.CharField()
    CpuTemp = serializers.CharField()
    GpuTemp = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class CoolerPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Size = serializers.CharField()
    RPM = serializers.CharField()
    LED = serializers.CharField()
    Noise = serializers.CharField()
    Color = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class GpuPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Manufacturer = serializers.CharField()
    Company = serializers.CharField()
    GPU = serializers.CharField()
    BoostClock = serializers.CharField()
    Memory = serializers.CharField()
    Length = serializers.CharField()
    BasicPower = serializers.CharField()
    MaximumPower = serializers.CharField()
    VRM = serializers.CharField()
    CoreTemp = serializers.CharField()
    Noise = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class MainboardPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    UseCase = serializers.CharField()
    Socket = serializers.CharField()
    ChipSet = serializers.CharField()
    Form = serializers.CharField()
    Memory = serializers.CharField()
    DIMM = serializers.CharField()
    M_2 = serializers.CharField()
    SATA = serializers.CharField()
    VRM = serializers.CharField()
    PowerLimit = serializers.CharField()
    Temp = serializers.CharField()
    Color = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class MemoryPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    Spec = serializers.CharField()
    UseCase = serializers.CharField()
    RamTiming = serializers.CharField()
    XMP = serializers.CharField()
    Color = serializers.CharField()
    RGB = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class PowerPriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    MaximumOutput = serializers.CharField()
    PLUS80 = serializers.CharField()
    Modular = serializers.CharField()
    FormFactor = serializers.CharField()
    CoolingFan = serializers.CharField()
    Bearing = serializers.CharField()
    Warranty = serializers.CharField()
    FullLoad = serializers.CharField()
    MaxRPM = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class StoragePriceDataSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    Model = serializers.CharField()
    Company = serializers.CharField()
    NAND = serializers.CharField()
    Capacity = serializers.CharField()
    Interface = serializers.CharField()
    FormFactor = serializers.CharField()
    DRAM = serializers.CharField()
    ReadPerformance = serializers.CharField()
    WritePerformance = serializers.CharField()
    Read4K = serializers.CharField()
    Write4K = serializers.CharField()
    MaximumTemp = serializers.CharField()
    ImageURL = serializers.CharField()
    Date = serializers.CharField()
    Shop = serializers.CharField()
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    AvgPriceLast45Days = serializers.CharField()
    Price = serializers.CharField()
    URL = serializers.CharField()
    LowestPrice = serializers.CharField()
    LowestShop = serializers.CharField()
    LowestURL = serializers.CharField()

class OrderListviewSerializer(serializers.Serializer):
    OrderID = serializers.CharField()
    UserID = serializers.CharField()
    CPU = serializers.CharField()
    GPU = serializers.CharField()
    Mainboard = serializers.CharField()
    Memory = serializers.CharField()
    Storage = serializers.CharField()
    PcCase = serializers.CharField()
    Cooler = serializers.CharField()
    Power = serializers.CharField()
    ImageURL = serializers.CharField()

class Price45DaysSerializer(serializers.Serializer):
    ComponentID = serializers.CharField()
    Type = serializers.CharField()
    day1 = serializers.CharField()
    day1shop = serializers.CharField()
    day2 = serializers.CharField()
    day2shop = serializers.CharField()
    day3 = serializers.CharField()
    day3shop = serializers.CharField()
    day4 = serializers.CharField()
    day4shop = serializers.CharField()
    day5 = serializers.CharField()
    day5shop = serializers.CharField()
    day6 = serializers.CharField()
    day6shop = serializers.CharField()
    day7 = serializers.CharField()
    day7shop = serializers.CharField()
