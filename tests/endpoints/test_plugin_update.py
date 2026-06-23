from cms.api import add_plugin
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase


class PluginUpdateAPITestCase(BaseCMSRestTestCase):
    def setUp(self):
        super().setUp()
        page = self.pages[0]
        self.placeholder = page.get_placeholders("en").first()
        self.text_plugin = add_plugin(
            self.placeholder,
            "TextPlugin",
            "en",
            body="<p>Original</p>",
        )
        self.non_text_plugin = add_plugin(
            self.placeholder,
            "DummyLinkPlugin",
            "en",
            label="Dummy link",
        )

    def test_patch_requires_authentication(self):
        response = self.client.patch(
            reverse("plugin-detail", kwargs={"language": "en", "pk": self.text_plugin.pk}),
            data={"body": "<p>Changed</p>"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_patch_updates_text_plugin(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            reverse("plugin-detail", kwargs={"language": "en", "pk": self.text_plugin.pk}),
            data={"body": "<p>Changed</p>"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["body"], "<p>Changed</p>")

    def test_patch_rejects_non_text_plugins(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            reverse("plugin-detail", kwargs={"language": "en", "pk": self.non_text_plugin.pk}),
            data={"body": "<p>Changed</p>"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
