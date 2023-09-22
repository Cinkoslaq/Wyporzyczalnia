from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class Category(models.Model):
    """Model reprezentujący kategorię maszyn."""
    # Pole do przechowywania nazwy kategorii maszyn.
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Machinery(models.Model):
    """Model reprezentujący maszynę."""
    # Pole do przechowywania nazwy maszyny.
    name = models.CharField(max_length=100)
    # Pole ManyToMany do przechowywania kategorii maszyn.
    categories = models.ManyToManyField(Category)
    # Pole do przechowywania ceny wynajmu maszyny za dzień.
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    # Pole ManyToMany do przechowywania komentarzy dotyczących maszyny.
    comments = models.ManyToManyField('Comments')

    def __str__(self):
        return self.name


class Rental(models.Model):
    """Model reprezentujący wynajem maszyn."""
    # Pole do przechowywania maszyn wynajętych w ramach tego wynajmu.
    machinery = models.ManyToManyField(Machinery)
    # Pole do przechowywania daty rozpoczęcia wynajmu.
    start_date = models.DateField()
    # Pole do przechowywania daty zakończenia wynajmu.
    end_date = models.DateField()

    def __str__(self):
        return f"Rental {self.id}"


class Delivery(models.Model):
    """Model reprezentujący dostawę maszyn w ramach wynajmu."""
    # Wybór rodzaju dostawy
    DELIVERY_CHOICES = (
        ('self-pickup', 'Self Pickup'),
        ('express-delivery', 'Express Delivery'),
        ('standard-delivery', 'Standard Delivery'),
    )
    # Relacja z modelem Rental: Każda dostawa jest powiązana z jednym wynajmem.
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, null=True)
    # Pole do przechowywania wybranego rodzaju dostawy.
    delivery_type = models.CharField(max_length=50, choices=DELIVERY_CHOICES)


class Company(models.Model):
    """Model reprezentujący firmę."""
    # Relacja z modelem User: Każda firma jest powiązana z jednym użytkownikiem.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Pole do przechowywania numeru NIP firmy.
    NIP = models.CharField(max_length=15)
    # Pole do przechowywania adresu firmy.
    address = models.CharField(max_length=200)
    # Pole do przechowywania opisu firmy.
    description = models.TextField()

    def __str__(self):
        return self.user.username


class Ratings(models.Model):
    """Model reprezentujący oceny wystawiane firmom."""
    # Relacja z modelem Company: Każda ocena jest powiązana z jedną firmą.
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Pole do przechowywania oceny.
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Ocena musi być większa lub równa 1."),
            MaxValueValidator(5, "Ocena musi być mniejsza lub równa 5.")
        ]
    )
    # Relacja z modelem User: Każda ocena jest powiązana z jednym użytkownikiem.
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    """Model reprezentujący komentarze do firm."""
    # Relacja z modelem Company: Każdy komentarz jest powiązany z jedną firmą.
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Pole do przechowywania treści komentarza.
    content = models.TextField()

