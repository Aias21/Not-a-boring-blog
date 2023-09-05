from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    new_data = data.copy()
    new_data["errors"] = ""
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        new_data["errors"] += 'Email already exists'
    ##
    if not password or len(password) < 8:
        new_data["errors"] += 'Password must have at least 8 characters and special characters.'
    ##
    if not username:
        new_data["errors"] += 'Username already exists'
    

    return new_data




def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True