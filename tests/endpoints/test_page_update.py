from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase


class PageUpdateAPITestCase(BaseCMSRestTestCase):
    def test_patch_requires_authentication(self):
        response = self.client.patch(
            reverse("page-detail", kwargs={"language": "en", "path": "page-0"}),
            data={"title": "Updated title"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_patch_updates_page_content(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            reverse("page-detail", kwargs={"language": "en", "path": "page-0"}),
            data={"title": "Updated title", "login_required": True},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated title")
        self.assertTrue(data["login_required"])

    def test_post_does_not_create_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("page-list", kwargs={"language": "en"}),
            data={"title": "Should not create"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 405)
