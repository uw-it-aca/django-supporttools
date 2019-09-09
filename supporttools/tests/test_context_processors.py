from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from supporttools.context_processors import has_google_analytics
from supporttools.tests import get_request


class TestContextProcessors(TestCase):

    def test_has_google_analytics(self):
        with self.settings(GOOGLE_ANALYTICS_KEY="ga_1234"):
            values = has_google_analytics(get_request())
            self.assertTrue(values["has_google_analytics"])
            self.assertEquals(values["GOOGLE_ANALYTICS_KEY"], "ga_1234")

    def test_missing_google_analytics(self):
        with self.settings(GOOGLE_ANALYTICS_KEY=None):
            values = has_google_analytics(get_request())
            self.assertFalse(values["has_google_analytics"])

    def test_user_agents(self):
        # No user agent
        response = self.client.get(reverse('supporttools_home'))
        self.assertContains(response, 'is_mobile: false', status_code=200)
        self.assertContains(response, 'is_tablet: false', status_code=200)
        self.assertContains(response, 'is_desktop: false', status_code=200)

        iphone_ua = ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) '
                     'AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 '
                     'Mobile/15A372 Safari/604.1')
        response = self.client.get(reverse('supporttools_home'),
                                   HTTP_USER_AGENT=iphone_ua)

        self.assertContains(response, 'is_mobile: true', status_code=200)
        self.assertContains(response, 'is_tablet: false', status_code=200)
        self.assertContains(response, 'is_desktop: false', status_code=200)

        kindle_ua = ('Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI '
                     'Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36')
        response = self.client.get(reverse('supporttools_home'),
                                   HTTP_USER_AGENT=kindle_ua)

        self.assertContains(response, 'is_mobile: false', status_code=200)
        self.assertContains(response, 'is_tablet: true', status_code=200)
        self.assertContains(response, 'is_desktop: false', status_code=200)

        firefox_ua = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) '
                      'Gecko/20100101 Firefox/15.0.1')
        response = self.client.get(reverse('supporttools_home'),
                                   HTTP_USER_AGENT=firefox_ua)

        self.assertContains(response, 'is_mobile: false', status_code=200)
        self.assertContains(response, 'is_tablet: false', status_code=200)
        self.assertContains(response, 'is_desktop: true', status_code=200)
