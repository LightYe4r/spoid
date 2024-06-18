from django.db import models

class Cpu(models.Model):
    cpu_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    process = models.CharField(max_length=100)
    socket = models.CharField(max_length=100)
    core = models.IntegerField()
    thread = models.IntegerField()
    clock = models.FloatField()
    boost = models.FloatField()
    memory = models.CharField(max_length=100)
    l3_cache = models.CharField(max_length=100)
    graphic = models.CharField(max_length=100)
    gpu_clock = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Memory(models.Model):
    memory_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    use_case = models.CharField(max_length=100)
    ram_timing = models.CharField(max_length=100)
    xmp = models.BooleanField()
    rgb = models.BooleanField()
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Cooler(models.Model):
    cooler_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    rpm = models.IntegerField()
    led = models.BooleanField()
    noise = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    cooling_fan = models.CharField(max_length=100)
    ladiator = models.CharField(max_length=100)
    cpu_cooler = models.CharField(max_length=100)
    power_size = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    chassis = models.CharField(max_length=100)
    cpu_temp = models.FloatField()
    gpu_temp = models.FloatField()
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Power(models.Model):
    power_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    maximum_output = models.IntegerField()
    eighty_plus = models.CharField(max_length=100)
    modular = models.BooleanField()
    form_factor = models.CharField(max_length=100)
    cooling_fan = models.CharField(max_length=100)
    bearing = models.CharField(max_length=100)
    warranty = models.IntegerField()
    full_load = models.FloatField()
    voltage_drop = models.FloatField()
    max_rpm = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return self.model

class MainBoard(models.Model):
    mainboard_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    use_case = models.CharField(max_length=100)
    socket = models.CharField(max_length=100)
    chipset = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    dimm = models.IntegerField()
    m_2 = models.IntegerField()
    sata = models.IntegerField()
    vrm = models.CharField(max_length=100)
    power_limit = models.CharField(max_length=100)
    temp = models.FloatField()
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Gpu(models.Model):
    gpu_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    boost_clock = models.FloatField()
    memory = models.CharField(max_length=100)
    length = models.IntegerField()
    basic_power = models.IntegerField()
    maximum_power = models.IntegerField()
    vrm = models.CharField(max_length=100)
    core_degree = models.FloatField()
    noise = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Storage(models.Model):
    storage_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    nand = models.CharField(max_length=100)
    interface = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=100)
    dram = models.CharField(max_length=100)
    read_performance = models.FloatField()
    write_performance = models.FloatField()
    four_k_read = models.FloatField()
    four_k_write = models.FloatField()
    persistent_write = models.FloatField()
    maximum_temp = models.FloatField()
    image_url = models.URLField()

    def __str__(self):
        return self.model

class Price(models.Model):
    price_id = models.AutoField(primary_key=True)
    cpu = models.ForeignKey(Cpu, on_delete=models.CASCADE, null=True, blank=True)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, null=True, blank=True)
    cooler = models.ForeignKey(Cooler, on_delete=models.CASCADE, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True)
    power = models.ForeignKey(Power, on_delete=models.CASCADE, null=True, blank=True)
    mainboard = models.ForeignKey(MainBoard, on_delete=models.CASCADE, null=True, blank=True)
    gpu = models.ForeignKey(Gpu, on_delete=models.CASCADE, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    shop = models.CharField(max_length=100)
    price = models.FloatField()
    url = models.URLField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'shop', 'cpu', 'memory', 'cooler', 'case', 'power', 'mainboard', 'gpu', 'storage'], name='unique_price')
        ]

    def __str__(self):
        return f"{self.date} - {self.shop} - {self.price}"

class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    cpu = models.ForeignKey(Cpu, on_delete=models.CASCADE, null=True, blank=True)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, null=True, blank=True)
    cooler = models.ForeignKey(Cooler, on_delete=models.CASCADE, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True)
    power = models.ForeignKey(Power, on_delete=models.CASCADE, null=True, blank=True)
    mainboard = models.ForeignKey(MainBoard, on_delete=models.CASCADE, null=True, blank=True)
    gpu = models.ForeignKey(Gpu, on_delete=models.CASCADE, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'cpu', 'memory', 'cooler', 'case', 'power', 'mainboard', 'gpu', 'storage'], name='unique_favorite')
        ]

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    cpu = models.ForeignKey(Cpu, on_delete=models.CASCADE)
    gpu = models.ForeignKey(Gpu, on_delete=models.CASCADE)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    cooler = models.ForeignKey(Cooler, on_delete=models.CASCADE)
    mainboard = models.ForeignKey(MainBoard, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    power = models.ForeignKey(Power, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'cpu', 'gpu', 'memory', 'cooler', 'mainboard', 'storage', 'case', 'power'], name='unique_order')
        ]

class OrderAlarm(models.Model):
    order_alarm_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'order'], name='unique_order_alarm')
        ]

class ComponentAlarm(models.Model):
    component_alarm_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    cpu = models.ForeignKey(Cpu, on_delete=models.CASCADE, null=True, blank=True)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, null=True, blank=True)
    cooler = models.ForeignKey(Cooler, on_delete=models.CASCADE, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True)
    power = models.ForeignKey(Power, on_delete=models.CASCADE, null=True, blank=True)
    mainboard = models.ForeignKey(MainBoard, on_delete=models.CASCADE, null=True, blank=True)
    gpu = models.ForeignKey(Gpu, on_delete=models.CASCADE, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'cpu', 'memory', 'cooler', 'case', 'power', 'mainboard', 'gpu', 'storage'], name='unique_component_alarm')
        ]
