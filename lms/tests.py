from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.moderator = User.objects.create(email='1@1.com', password='123123')
        group = Group.objects.create(name='moderator')
        self.moderator.groups.add(group)
        self.moderator.save()

        self.user = User.objects.create(email='2@2.com', password='321123')
        self.user.save()

    def test_course_create(self):
        data = {"title": "course1", "description": "desc1"}
        url = reverse('lms:course-list')
        self.client.force_login(user=self.moderator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_destroy(self):
        course = Course.objects.create(title="course1", description="desc1", owner=self.user)
        url = reverse('lms:course-detail', kwargs={'pk': course.pk})
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create(id=1, email='test@test.com', password='123123')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='test_course', description='test_desc')
        self.lesson = Lesson.objects.create(title='test_lesson', description='test_desc',
                                            video_link='https://youtube.com/',
                                            course=self.course, owner=self.user)

    def test_create_lesson(self):
        data = {'title': 'test', 'description': 'test',
                'course': self.course.id, 'url': 'https://youtube.com/',
                'owner': self.user.id}
        url = reverse('lms:create_lesson')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title=data['title']).exists())

    def test_retrieve_lesson(self):
        url = reverse('lms:view_lesson', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        url = reverse('lms:update_lesson', kwargs={'pk': self.lesson.pk})
        data = {'title': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data['title'])

    def test_delete_lesson(self):
        self.moderator = User.objects.create(email='moder@test.com', password='123123')
        group = Group.objects.create(name='moderator')
        self.moderator.groups.add(group)
        self.moderator.save()

        self.client.force_authenticate(user=self.moderator)

        url = reverse('lms:delete_lesson', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
