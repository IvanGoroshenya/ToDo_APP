from passlib.context import CryptContext

# настройка для использования алгоритма bcrypt, который является методом хэширования.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция принимает пароль пользователя в виде строки
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Функция используется для проверки пароля пользователя.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
