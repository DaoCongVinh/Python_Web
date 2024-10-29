from operator import mod
from django.db import models

# Create your models here.
class Student(models.Model):
    # Tên table liên kết với class model: <tên app viết thường>_<tên class viết thường>
    # name, age, gender, email, phone
    # name, email, phone (lấy chữ 0): TEXT
    # age: INTEGER
    # gender: BOOLEAN
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.BooleanField() # True: Nam, False: Nữ
    email = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    address = models.TextField(default="Hồ Chí Minh") #textfield không giới hạn về độ dài


    def __str__(self):
        return self.name


# Những lệnh kiểm tra với thay đổi của models.py

# 1. Kiểm tra xem mình có thay đổi gì hay không? python manage.py makemigrations
# Không có tên app thì sẽ là toàn bộ các app
# 2. Xem các thay đổi dưới dạng SQL command? python manage.py sqlmigrate <tên app><số tạo ra ở command trên> myapp 0001

# 3. Apply các thay đổi xuống Database. python manage.py migrate

# Quan hệ 1-1:

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} is a Place"

    class Meta: # đổi tên của table
        db_table = "Place" # 'db_table' định nghĩa tên tuỳ chọn của Table trong DB
    
class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE, # 'on_delete: CASCADE' khi xoá khoá chính của liên kết FK thì nó sẽ tự động xoá hết FK
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.name} the restaurant"

    class Meta:
        db_table = "Restaurant"

# Quan hệ nhiều-1:

# class Reporter(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()

#     def __str__(self):
#         return "%s %s" % (self.first_name, self.last_name)

#     class Meta:
#         db_table = "Reporter"

# class Article(models.Model):
#     headline = models.CharField(max_length=100)
#     pub_date = models.DateField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.headline

#     class Meta:
#         ordering = ['headline']
#         db_table = "Article"

# Quan hệ nhiều-nhiều:
# class Publication(models.Model):
#     title = models.CharField(max_length=30)

#     class Meta:
#         ordering = ['title'] # Dùng để sắp xếp, tăng dần ['title']/['-title'] giảm dần
#         db_table = "Publication"

#     def __str__(self):
#         return self.title

# class Article(models.Model):
#     headline = models.CharField(max_length=100)
#     publications = models.ManyToManyField(Publication)

#     class Meta:
#         ordering = ['headline']
#         db_table = "Article"

#     def __str__(self):
#         return self.headline

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title'] # Dùng để sắp xếp, tăng dần ['title']/['-title'] giảm dần
        db_table = "Publication"

    def __str__(self):
        return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']
        db_table = "Article"

    def __str__(self):
        return self.headline


class Pet(models.Model):
    TYPE_CHOICES = (
        ('cat', 'cat'),
        ('dog', 'dog')
    )
    id = models.CharField('Mã Thú Cưng', max_length=10, primary_key=True)
    name = models.CharField('Tên Thú Cưng', max_length=30)
    age = models.IntegerField('Tuổi')
    type = models.CharField('Loại', max_length=3, choices=TYPE_CHOICES)
    weight = models.FloatField('Cân Nặng')
    length = models.IntegerField('Chiều Cao')
    color = models.CharField('Màu Sắc', max_length=7) # #00FF1A
    vacinated = models.BooleanField()
    dewormed = models.BooleanField()
    sterilized = models.BooleanField()

    class Meta:
        db_table = "Pet"