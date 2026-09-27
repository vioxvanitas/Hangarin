from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Priority, Task


class DashboardTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.client.force_login(user_model.objects.create_user(username="owner"))

	def test_dashboard_shows_status_and_overdue_totals(self):
		priority = Priority.objects.create(name="Normal")
		category = Category.objects.create(name="Work")
		overdue_deadline = timezone.now() - timedelta(days=1)
		Task.objects.create(
			title="Pending task",
			description="Needs attention",
			status="Pending",
			deadline=overdue_deadline,
			priority=priority,
			category=category,
		)
		Task.objects.create(
			title="Active task",
			description="Currently underway",
			status="In Progress",
			priority=priority,
			category=category,
		)
		Task.objects.create(
			title="Finished task",
			description="Already done",
			status="Completed",
			deadline=overdue_deadline,
			priority=priority,
			category=category,
		)

		response = self.client.get(reverse("dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["pending_count"], 1)
		self.assertEqual(response.context["in_progress_count"], 1)
		self.assertEqual(response.context["overdue_count"], 1)
		self.assertContains(response, 'id="task-search"')
		self.assertContains(response, "Pending task")


class AuthenticationTests(TestCase):
	def test_anonymous_user_is_redirected_to_login(self):
		response = self.client.get(reverse("dashboard"))

		self.assertRedirects(
			response,
			f"{reverse('login')}?next={reverse('dashboard')}",
		)

	def test_user_can_log_in_and_view_dashboard(self):
		user_model = get_user_model()
		user_model.objects.create_user(username="owner", password="test-password-123")

		response = self.client.post(
			reverse("login"),
			{"username": "owner", "password": "test-password-123"},
		)

		self.assertRedirects(response, reverse("dashboard"))
		self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

	def test_user_can_log_out(self):
		user_model = get_user_model()
		user_model.objects.create_user(username="owner", password="test-password-123")
		self.client.login(username="owner", password="test-password-123")

		response = self.client.post(reverse("logout"))

		self.assertRedirects(response, reverse("login"))
		self.assertRedirects(
			self.client.get(reverse("dashboard")),
			f"{reverse('login')}?next={reverse('dashboard')}",
		)
