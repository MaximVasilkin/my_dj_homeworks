import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student
from random import choice


def __get_data(url, client, params=False):
    response = client.get(url, data=params)
    data = response.json()
    return response.status_code, data

@pytest.fixture
def url():
    return r'/api/v1/courses/'

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

# @pytest.fixture
# def course():
#     return Course.objects.create('Python')

@pytest.mark.django_db
def test_get_new_course(client, course_factory, url):
    course = course_factory()
    course_id = course.id
    url += f'{course_id}/'
    status, data = __get_data(url, client)
    assert status == 200
    assert data['id'] == course.id


@pytest.mark.django_db
def test_get_list_of_courses(client, course_factory, url):
    courses = course_factory(_quantity=30)
    status, data = __get_data(url, client)
    for index, course in enumerate(data):
        assert course['id'] == courses[index].id
    assert status == 200


@pytest.mark.django_db
def test_course_filter_id(client, course_factory, url):
    courses = course_factory(_quantity=30)
    random_course = choice(courses)
    random_course_id = random_course.id
    params = {'id': random_course_id}
    status, data = __get_data(url, client, params=params)
    assert data[0]['id'] == random_course_id
    assert status == 200


@pytest.mark.django_db
def test_course_filter_name(client, course_factory, url):
    courses = course_factory(_quantity=30)
    random_course = choice(courses)
    random_course_name = random_course.name
    params = {'name': random_course_name}
    status, data = __get_data(url, client, params=params)
    assert data[0]['name'] == random_course_name
    assert status == 200


@pytest.mark.django_db
def test_course_create(client, url):
    count = Course.objects.count()
    course_name = 'Python_course'
    data = {'name': course_name}
    response = client.post(url, data=data)
    new_course = Course.objects.filter(name=course_name)[0]
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert new_course.name == course_name

@pytest.mark.django_db
def test_course_update(client, url, course_factory, student_factory):
    course = course_factory()
    student = student_factory()
    len_before = len(course.students.all())
    data = {'students': [student.id]}
    url += f'{course.id}/'
    response = client.patch(url, data=data)
    len_after = len(course.students.all())
    assert len_before == len_after - 1
    assert response.status_code == 200

@pytest.mark.django_db
def test_course_delete(client, url, course_factory, student_factory):
    course = course_factory()
    url += f'{course.id}/'
    response = client.delete(url)
    deleted_course = Course.objects.filter(id=course.id)
    assert not deleted_course
    assert response.status_code == 204
