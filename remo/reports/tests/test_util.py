from django.contrib.auth.models import User
from nose.tools import eq_
from test_utils import TestCase

from remo.reports.utils import REPORTS_PERMISSION_LEVEL, get_reports_for_year


class UtilsTest(TestCase):
    fixtures = ['demo_users.json', 'demo_reports.json']

    def test_get_reports_anonymous(self):
        """Test get reports utility as anonymous."""
        user = User.objects.get(username="rep")
        reports = get_reports_for_year(user, start_year=2011, end_year=2012)

        eq_(len(reports[2011]), 12)
        for i in range(0, 12):
            eq_(reports[2011][i]['report'], None)
        eq_(len(reports[2012]), 12)
        for i in range(0, 2):
            self.assertIsNotNone(reports[2012][i]['report'])
            eq_(reports[2012][i]['class'], 'exists')
        for i in range(2, 12):
            self.assertIsNone(reports[2012][i]['report'])
            eq_(reports[2012][i]['class'], 'unavailable')

    def test_get_reports_owner(self):
        """Test get reports utility as owner."""
        user = User.objects.get(username="rep")
        reports = get_reports_for_year(
            user, start_year=2011, end_year=2012,
            permission=REPORTS_PERMISSION_LEVEL['owner'])

        eq_(len(reports[2011]), 12)
        eq_(len(reports[2012]), 12)
        for i in range(0, 7):
            self.assertIsNone(reports[2011][i]['report'])
            eq_(reports[2011][i]['class'], 'unavailable')
        for i in range(7, 12):
            self.assertIsNone(reports[2011][i]['report'])
            eq_(reports[2011][i]['class'], 'editable')
        for i in range(0, 2):
            self.assertIsNotNone(reports[2012][i]['report'])
            eq_(reports[2012][i]['class'], 'exists')
