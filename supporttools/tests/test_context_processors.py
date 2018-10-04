from django.test import TestCase
from django.conf import settings
from supporttools.context_processors import (
    has_less_compiled, has_google_analytics)
from supporttools.tests import get_request


class TestContextProcessors(TestCase):

    def test_less_none(self):
        with self.settings(COMPRESS_PRECOMPILERS=None):
            values = has_less_compiled(get_request())
            self.assertFalse(values["has_less_compiled"])

    def test_less_empty(self):
        with self.settings(COMPRESS_PRECOMPILERS=()):
            values = has_less_compiled(get_request())
            self.assertFalse(values["has_less_compiled"])

    def test_less_other_precompilers(self):
        with self.settings(COMPRESS_PRECOMPILERS=(
                ('text/coffeescript',
                 'coffee --compile --stdio'),
                ('text/foobar',
                 'path.to.MyPrecompilerFilter'),)):
            values = has_less_compiled(get_request())
            self.assertFalse(values["has_less_compiled"])

    def test_less_has_less_precompiler(self):
        with self.settings(COMPRESS_PRECOMPILERS=(
                ('text/coffeescript',
                 'coffee --compile --stdio'),
                ('text/foobar',
                 'path.to.MyPrecompilerFilter'),
                ('text/less', 'lessc {infile} {outfile}'),)):
            values = has_less_compiled(get_request())
            self.assertTrue(values["has_less_compiled"])

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
        request = get_request()
        self.assertFalse(request.user_agent.is_mobile)
        self.assertFalse(request.user_agent.is_tablet)
        self.assertFalse(request.user_agent.is_pc)
        self.assertFalse(request.user_agent.is_bot)

        iphone_ua = ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) '
                     'AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 '
                     'Mobile/15A372 Safari/604.1')
        request = get_request(user_agent=iphone_ua)
        self.assertTrue(request.user_agent.is_mobile)
        self.assertFalse(request.user_agent.is_tablet)
        self.assertFalse(request.user_agent.is_pc)
        self.assertFalse(request.user_agent.is_bot)

        kindle_ua = ('Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI '
                     'Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36')
        request = get_request(user_agent=kindle_ua)
        self.assertFalse(request.user_agent.is_mobile)
        self.assertTrue(request.user_agent.is_tablet)
        self.assertFalse(request.user_agent.is_pc)
        self.assertFalse(request.user_agent.is_bot)

        firefox_ua = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) '
                      'Gecko/20100101 Firefox/15.0.1')
        request = get_request(user_agent=firefox_ua)
        self.assertFalse(request.user_agent.is_mobile)
        self.assertFalse(request.user_agent.is_tablet)
        self.assertTrue(request.user_agent.is_pc)
        self.assertFalse(request.user_agent.is_bot)
