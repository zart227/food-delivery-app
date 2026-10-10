from datetime import date, datetime, time, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import Order
from .tasks import generate_daily_report


@override_settings(
    TIME_ZONE="Europe/Moscow",
    USE_TZ=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class DailyReportTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="report-user", email="report@example.com",
        )
        self.today = date(2025, 1, 15)
        self.yesterday = self.today - timedelta(days=1)
        self.tz = timezone.get_default_timezone()

    def create_order(self, day, at=time.min, price="100.00", status="completed"):
        order = Order.objects.create(
            user=self.user, total_price=Decimal(price), status=status,
            address="Test address", phone="1234567890",
        )
        # auto_now_add ignores supplied creation timestamps.
        Order.objects.filter(pk=order.pk).update(
            created_at=datetime.combine(day, at, tzinfo=self.tz),
        )
        # Discard confirmation emails emitted by the order creation signal.
        mail.outbox.clear()
        return order

    def assert_report(self, result, day, count, revenue):
        self.assertEqual(
            result, f"Generated daily report: {count} orders, {revenue} ₽ revenue.",
        )
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Ежедневный отчет о заказах за {day}")
        self.assertEqual(
            email.body,
            f"Отчет за {day}\nВыполнено заказов: {count}\nОбщая выручка: {revenue} ₽",
        )
        self.assertEqual(email.to, ["admin@example.com"])

    def test_default_reports_yesterday_in_settings_timezone(self):
        self.create_order(self.yesterday, time(23, 59), price="125.50")
        self.create_order(self.today, time(0, 1), price="999.00")
        midnight = datetime.combine(self.today, time.min, tzinfo=self.tz)
        # This instant is still yesterday in UTC. An active timezone must not
        # change the reporting calendar configured in settings.TIME_ZONE.
        with timezone.override("UTC"), patch("django.utils.timezone.now", return_value=midnight):
            result = generate_daily_report()
        self.assert_report(result, self.yesterday, 1, "125.50")

    def test_range_includes_start_and_excludes_end(self):
        self.create_order(self.yesterday, price="12.34")
        self.create_order(self.yesterday - timedelta(days=1), time(23, 59, 59))
        self.create_order(self.today, price="999.00")
        result = generate_daily_report(report_date=self.yesterday)
        self.assert_report(result, self.yesterday, 1, "12.34")

    def test_only_completed_orders_contribute_to_count_and_revenue(self):
        self.create_order(self.yesterday, price="10.25")
        self.create_order(self.yesterday, price="20.50")
        self.create_order(self.yesterday, price="500.00", status="pending")
        self.create_order(self.yesterday, price="600.00", status="processing")
        result = generate_daily_report(report_date=self.yesterday)
        self.assert_report(result, self.yesterday, 2, "30.75")

    def test_empty_day_returns_zeros_and_sends_email(self):
        result = generate_daily_report(report_date=self.yesterday)
        self.assert_report(result, self.yesterday, 0, "0")

    def test_explicit_date_recalculates_historical_day(self):
        historical_day = date(2024, 6, 1)
        self.create_order(historical_day, price="75.00")
        self.create_order(self.yesterday, price="999.00")
        result = generate_daily_report(report_date=historical_day)
        self.assert_report(result, historical_day, 1, "75.00")

    def test_iso_date_for_celery_json_arguments(self):
        self.create_order(self.yesterday, price="42.00")
        result = generate_daily_report(report_date=self.yesterday.isoformat())
        self.assert_report(result, self.yesterday, 1, "42.00")

    @override_settings(TIME_ZONE="Europe/Berlin")
    def test_daylight_saving_day_uses_two_local_midnights(self):
        self.tz = timezone.get_default_timezone()
        day = date(2025, 3, 30)  # 23-hour day when daylight saving starts.
        self.create_order(day, time(23, 59), price="15.00")
        self.create_order(day + timedelta(days=1), price="999.00")
        result = generate_daily_report(report_date=day)
        self.assert_report(result, day, 1, "15.00")
