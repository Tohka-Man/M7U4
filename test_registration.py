import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."


def test_authenticate_user(setup_database):
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password123')==  True


def test_authenticate_user1(setup_database):
    assert authenticate_user('testuser_1', 'password1231')==  False
    

def test_authenticate_user2(setup_database):
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password1234')==  False


def test_add_new_user1(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    user = add_user('testuser', 'testuser1@example.com', 'password1234')
    assert not user, "Пользователь не должен быть добавлен в базу данных."


def test_display_users(setup_database, capsys):
    add_user('testuser', 'testuser@example.com', 'password123')
    display_users()
    a=capsys.readouterr()
    assert 'testuser' in a.out, "Есть логин"
    assert 'password123' not in a.out, "Нет пароля"

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""