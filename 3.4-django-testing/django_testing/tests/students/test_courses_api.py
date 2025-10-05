import pytest
from django.core.exceptions import ValidationError
from students.models import Course
from django.urls import reverse

@pytest.mark.django_db
def test_get_course(client, courses_factory):
    """
    Тестируем успешное получение конкретного курса.
    """
    # Создаем курс через фабрику
    course = courses_factory(name = "Python Basics")

    # Строим URL и отправляем GET-запрос
    url = reverse('courses-list')
    response = client.get(url)
    resp_json = response.json()

    # Проверяем статус ответа и данные
    assert response.status_code == 200
    assert len(resp_json) == 1
    assert resp_json[0]['name'] == course.name


@pytest.mark.django_db
def test_get_all_courses(client, courses_factory):
    """
    Тестируем успешное получение списка курсов.
    """
    # Создаем курсы через фабрику
    courses = courses_factory(_quantity=3)

    # Отправляем GET-запрос на получение списка курсов
    url = reverse('courses-list')
    response = client.get(url)
    resp_json = response.json()

    # Проверяем количество полученных записей и их названия
    assert response.status_code == 200
    assert len(resp_json) == 3
    expected_names = sorted(item.name for item in courses)
    received_names = sorted(item["name"] for item in resp_json)
    assert received_names == expected_names


@pytest.mark.django_db
def test_filter_courses_by_id(client, courses_factory):
    """
    Тестируем фильтрацию курсов по идентификатору.
    """
    # Создаем два курса
    course1 = courses_factory(name = "Python")
    course2 = courses_factory(name = "React Development")

    # Применяем фильтр по ID первого курса
    url = f'{reverse('courses-list')}?id={course1.pk}'
    response = client.get(url)

    # Проверяем наличие нужного курса в результате
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Python"


@pytest.mark.django_db
def test_filter_courses_by_name(client, courses_factory):
    """
    Тестируем фильтрацию курсов по наименованию.
    """
    course1 = courses_factory(name = "Python Fullstack")
    course2 = courses_factory(name = "Data Science with Python")

    # Применяем фильтр по ID первого курса
    url = f'{reverse('courses-list')}?name={course1.name}'
    response = client.get(url)

    # Проверяем наличие нужного курса в результате
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Python Fullstack"


@pytest.mark.django_db
def test_create_course(client, courses_factory):
    """
    Тестируем успешность создания курса post запросом.
    """
    payload = {"name": "Data Science with Python"}
    url = reverse('courses-list')
    response = client.post(url, payload)

    # Проверяем наличие нужного курса в результате
    assert response.status_code == 201
    assert Course.objects.filter(name = 'Data Science with Python').exists()
    created_course = Course.objects.get(name = 'Data Science with Python')
    assert created_course.name == payload['name']


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    """
    Тестируем обновление курса.
    """

    course = courses_factory(name = "Python")
    payload = {"name": "Python advanced"}
    url = f'{reverse('courses-list')}{course.pk}/'
    response = client.patch(url, payload)

    # Проверяем успех обновления и новые данные
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "Python advanced"


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    """
    Тестируем удаление курса.
    """

    # Создаем курс
    course = courses_factory(name = "Python Fullstack")
    url = f'{reverse('courses-list')}{course.pk}/'
    # Удаляем курс
    response = client.delete(url)

    # Проверяем успех удаления и отсутствие в БД
    assert response.status_code == 204
    assert not Course.objects.filter(name = "Python Fullstack").exists()


@pytest.mark.parametrize("count_students_on_course, expected_result", [
    (19, True),      # Допустимый случай
    (20, True),      # Граница допустимых значений
    (21, False),     # Превышаем лимит
])

@pytest.mark.django_db
def test_validate_max_students(count_students_on_course, expected_result, settings, students_factory):
    """
    Проверяем работу валидатора на ограничение количества студентов на курсе.
    """

    # Создаем курс
    course = Course.objects.create(name="Test Course")

    # Создаем заданное количество студентов
    students_list = [students_factory() for _ in range(count_students_on_course)]

    # Добавляем студентов
    try:
        course.students.set(students_list)
        # вызываем валидацию
        course.clean()
        validation_passed = True
    except ValidationError:
        validation_passed = False

    # Проверяем результат
    assert validation_passed == expected_result