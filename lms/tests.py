from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course
from users.models import User


class CourseTestCase(TestCase):
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
