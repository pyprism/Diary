import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        email="test@example.com",
        password="testpassword123"
    )
    assert user.email == "test@example.com"
    assert user.is_active
    assert not user.is_staff
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_user_email_unique():
    User.objects.create_user(
        email="unique@example.com",
        password="testpassword123"
    )
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="unique@example.com",
            password="testpassword123"
        )


@pytest.mark.django_db
def test_superuser_creation():
    admin_user = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpassword123"
    )
    assert admin_user.email == "admin@example.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
