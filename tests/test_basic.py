import pytest
from django.urls import reverse
from Wyporzyczalnia_app.models import Machinery, Comments

@pytest.mark.django_db
def test_add_machinery(client):
    # Test dodawania maszyny
    data = {
        'name': 'Nowa Maszyna',
        'rental_price_per_day': 200,
        'categories': 'maszyny budowlane,maszyny rolnicze,transport',  # Kategorie oddzielone przecinkami
    }
    response = client.post(reverse('add_machinery'), data)
    # Oczekujemy kodu 200, jeśli widok wyświetla potwierdzenie dodania maszyny
    assert response.status_code == 200




@pytest.mark.django_db
def test_view_machinery_list(client):
    # Test przeglądania listy maszyn
    Machinery.objects.create(name='Maszyna 1', rental_price_per_day=150)
    Machinery.objects.create(name='Maszyna 2', rental_price_per_day=180)
    response = client.get(reverse('machinery_list'))
    assert response.status_code == 200
    assert 'Maszyna 1' in str(response.content)
    assert 'Maszyna 2' in str(response.content)

@pytest.mark.django_db
def test_delete_machinery(client):
    # Test usuwania maszyny
    machinery = Machinery.objects.create(name='Maszyna do usunięcia', rental_price_per_day=250)
    response = client.post(reverse('delete_machinery', args=[machinery.id]))
    assert response.status_code == 302  # Oczekujemy przekierowania
    assert not Machinery.objects.filter(name='Maszyna do usunięcia').exists()  # Oczekujemy, że maszyna została usunięta

@pytest.mark.django_db
def test_add_comment(client):
    # Test dodawania komentarza
    machinery = Machinery.objects.create(name='Maszyna z komentarzem', rental_price_per_day=300)
    response = client.post(reverse('add_comment', args=[machinery.id]), {'text': 'To jest komentarz'})
    # Oczekujemy kodu 302, jeśli widok przekierowuje użytkownika
    assert response.status_code == 302

