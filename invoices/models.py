
from django.db import models

class Customer(models.Model):
	customer_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=255)
	company = models.CharField(max_length=255, blank=True)
	address = models.CharField(max_length=255)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	phone = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return f"{self.name} ({self.company})"

class Order(models.Model):
	invoice_number = models.IntegerField(unique=True)
	date = models.DateField()
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	payment_terms = models.CharField(max_length=100)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"Invoice {self.invoice_number} for {self.customer}"

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	item_name = models.CharField(max_length=255)
	hours = models.DecimalField(max_digits=7, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	sum = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.item_name} ({self.order})"

# Create your models here.
