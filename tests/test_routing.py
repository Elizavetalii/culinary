from django.test import SimpleTestCase
from django.urls import Resolver404, resolve


class RoutingTests(SimpleTestCase):
    def test_portal_manager_routes_are_registered(self):
        for path in ["/manager/", "/manager/clients/", "/manager/orders/"]:
            with self.subTest(path=path):
                try:
                    match = resolve(path)
                except Resolver404 as exc:
                    self.fail(f"{path} is not registered: {exc}")
                self.assertTrue(match.func)
