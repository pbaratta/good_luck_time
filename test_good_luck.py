"""
"""


import good_luck
import unittest

def time_disp_to_time_tup(time_disp):
	""" return tuple of integers from within the string

	'3:46' => (3,4,6)
	'4:45' => (4,4,5)
	'10:49' => (1,0,4,9)
	"""

	return tuple(
		int(char)
		for char in time_disp
		if '0' <= char <= '9'
	)


class GoodLuckTestCase(unittest.TestCase):
	" parent class for good luck tests "

	good_luck_tester = None  # point to method being tested (set later...)
	i_care_about_reasons = True  # should we check the reasons or just lucky or not

	def setUp(self):  # pragma: no cover
		" before the tests are run, which method are we testing? "
		raise NotImplementedError('need to set good_luck_tester in setUp before tests are run')

	def get_lucky_result(self, time_disp):
		" run good_luck_tester on the given time "
		time_tup = time_disp_to_time_tup(time_disp)
		lucky_result = self.good_luck_tester(time_tup)
		return lucky_result

	def assertLuckyReason(self, time_disp, given_reason):
		" check that the time is lucky, and that the reason matches "
		is_lucky, real_reason = self.get_lucky_result(time_disp)
		self.assertTrue(is_lucky)
		if self.i_care_about_reasons:
			self.assertEqual(real_reason, given_reason)

	def assertNotLucky(self, time_disp):
		" check that the time is unlucky "
		is_lucky, _ = self.get_lucky_result(time_disp)
		self.assertFalse(is_lucky)

	def assertLuckyReasonSet(self, time_disp, given_reason_set):
		" check that the time is lucky, and that ALL the reasons are correct "
		is_lucky, real_reason = self.get_lucky_result(time_disp)
		self.assertTrue(is_lucky)

		if self.i_care_about_reasons:
			real_reason_set = set(real_reason.split(", "))
			self.assertEqual(real_reason_set, given_reason_set)


class TestSame(GoodLuckTestCase):
	def setUp(self):
		self.good_luck_tester = good_luck.is_same
		# self.i_care_about_reasons = True

	def test_same(self):
		SAME = 'repeated digit'
		self.assertLuckyReason('1:11', SAME)
		self.assertLuckyReason('4:44', SAME)
		self.assertLuckyReason('11:11', SAME)
		self.assertLuckyReason('22:22', SAME)

	def test_not_same(self):
		self.assertNotLucky('3:46')
		self.assertNotLucky('4:45')
		self.assertNotLucky('4:54')  # want to fail sameness test
		self.assertNotLucky('5:44')
		self.assertNotLucky('12:35')
		self.assertNotLucky('22:23')

class TestSteps(GoodLuckTestCase):
	def setUp(self):
		self.good_luck_tester = good_luck.is_steps
		# self.i_care_about_reasons = True

	def test_inc(self):
		INC = 'incrementing'
		self.assertLuckyReason('1:23', INC)
		self.assertLuckyReason('3:45', INC)
		self.assertLuckyReason('12:34', INC)
		self.assertLuckyReason('23:45', INC)

	def test_dec(self):
		DEC = 'decrementing'
		self.assertLuckyReason('2:10', DEC)
		self.assertLuckyReason('4:32', DEC)
		self.assertLuckyReason('6:54', DEC)

	def test_not_steps(self):
		self.assertNotLucky('1:24')
		self.assertNotLucky('1:35')  # delta must be 1 or -1
		self.assertNotLucky('1:47')  # delta must be 1 or -1
		self.assertNotLucky('2:53')
		self.assertNotLucky('11:53')
		self.assertNotLucky('19:04')

class TestPalindrome(GoodLuckTestCase):
	def setUp(self):
		self.good_luck_tester = good_luck.is_palindrome
		# self.i_care_about_reasons = True

	def test_palin(self):
		PALIN = 'palindrome'
		self.assertLuckyReason('1:11', PALIN)
		self.assertLuckyReason('1:21', PALIN)
		self.assertLuckyReason('3:03', PALIN)
		self.assertLuckyReason('6:36', PALIN)
		self.assertLuckyReason('9:19', PALIN)

	def test_not_palin(self):
		self.assertNotLucky('6:28')
		self.assertNotLucky('6:44')
		self.assertNotLucky('8:15')
		self.assertNotLucky('9:00')
		self.assertNotLucky('12:25')


class TestMathProblem(GoodLuckTestCase):
	def setUp(self):
		self.good_luck_tester = good_luck.is_math_problem
		# self.i_care_about_reasons = True

	def test_math_easy(self):
		# one reason
		self.assertLuckyReasonSet('3:58', set(['3+5=8']))  # format a+b=c (29 instances)
		self.assertLuckyReasonSet('9:00', set(['9*0=0']))  # format a*b=c (14 instances)
		self.assertLuckyReasonSet('3:52', set(['3=5-2']))  # format a=b-c (9 instances)
		self.assertLuckyReasonSet('11:13', set(['1+1+1=3']))  # format a+b+c=d (7 instances)
		self.assertLuckyReasonSet('12:52', set(['1+2=5-2']))  # format a+b=c-d (4 instances)
		self.assertLuckyReasonSet('12:44', set(['1=2-4/4']))  # format a=b-c/d (3 instances)
		self.assertLuckyReasonSet('12:49', set(['1+2*4=9']))  # format a+b*c=d (2 instances)

	def test_math_two_reasons(self):
		# two reasons
		self.assertLuckyReasonSet('9:18', set(['9-1=8', '9=1+8']))  # format a-b=c, a=b+c (29 instances)
		self.assertLuckyReasonSet('9:33', set(['9/3=3', '9=3*3']))  # format a/b=c, a=b*c (5 instances)
		self.assertLuckyReasonSet('1:33', set(['1*3=3', '1=3/3']))  # format a*b=c, a=b/c (4 instances)
		self.assertLuckyReasonSet('11:38', set(['1_1-3=8', '1_1=3+8']))  # format a_b-c=d, a_b=c+d (8 instances)
		self.assertLuckyReasonSet('10:06', set(['1*0=0*6', '1*0=0/6']))  # format a*b=c*d, a*b=c/d (8 instances)
		self.assertLuckyReasonSet('10:25', set(['1_0/2=5', '1_0=2*5']))  # format a_b/c=d, a_b=c*d (3 instances)
		self.assertLuckyReasonSet('12:54', set(['1-2+5=4', '1=2-5+4']))  # format a-b+c=d, a=b-c+d (2 instances)
		self.assertLuckyReasonSet('12:45', set(['1-2=4-5', '1=2+4-5']))  # format a-b=c-d, a=b+c-d (2 instances)

	def test_math_three_reasons(self):
		# three reasons
		self.assertLuckyReasonSet('2:12', set(['2*1=2', '2/1=2', '2=1*2']))  # format a*b=c, a/b=c, a=b*c (8 instances)
		self.assertLuckyReasonSet('2:20', set(['2-2=0', '2=2+0', '2=2-0']))  # format a-b=c, a=b+c, a=b-c (5 instances)
		self.assertLuckyReasonSet('4:41', set(['4/4=1', '4=4*1', '4=4/1']))  # format a/b=c, a=b*c, a=b/c (4 instances)
		self.assertLuckyReasonSet('10:30', set(['1*0*3=0', '1*0/3=0', '1*0=3*0']))  # format a*b*c=d, a*b/c=d, a*b=c*d (4 instances)
		self.assertLuckyReasonSet('11:50', set(['1-1=5*0', '1=1+5*0', '1=1-5*0']))  # format a-b=c*d, a=b+c*d, a=b-c*d (3 instances)
		self.assertLuckyReasonSet('11:45', set(['1*1+4=5', '1/1+4=5', '1+1*4=5']))  # format a*b+c=d, a/b+c=d, a+b*c=d (3 instances)
		self.assertLuckyReasonSet('11:32', set(['1*1=3-2', '1/1=3-2', '1=1*3-2']))  # format a*b=c-d, a/b=c-d, a=b*c-d (3 instances)

	def test_math_lotsa_reasons(self):
		# at least four reasons
		self.assertLuckyReasonSet('9:09', set(['9+0=9', '9-0=9', '9=0_9', '9=0+9']))  # format a+b=c, a-b=c, a=b_c, a=b+c (9 instances)
		self.assertLuckyReasonSet('10:23', set(['1+0_2=3', '1+0+2=3', '1-0+2=3', '1=0-2+3']))  # format a+b_c=d, a+b+c=d, a-b+c=d, a=b-c+d (5 instances)
		self.assertLuckyReasonSet('10:32', set(['1+0=3-2', '1-0=3-2', '1=0_3-2', '1=0+3-2']))  # format a+b=c-d, a-b=c-d, a=b_c-d, a=b+c-d (3 instances)
		self.assertLuckyReasonSet('11:08', set(['1-1=0*8', '1-1=0/8', '1=1+0*8', '1=1+0/8', '1=1-0*8', '1=1-0/8']))  # format a-b=c*d, a-b=c/d, a=b+c*d, a=b+c/d, a=b-c*d, a=b-c/d (6 instances)
		self.assertLuckyReasonSet('10:51', set(['1+0*5=1', '1+0/5=1', '1-0*5=1', '1-0/5=1', '1=0*5+1', '1=0/5+1']))  # format a+b*c=d, a+b/c=d, a-b*c=d, a-b/c=d, a=b*c+d, a=b/c+d (3 instances)
		self.assertLuckyReasonSet('10:22', set(['1*0_2=2', '1*0+2=2', '1*0=2-2', '1+0=2/2', '1-0=2/2', '1=0_2/2', '1=0+2/2']))  # format a*b_c=d, a*b+c=d, a*b=c-d, a+b=c/d, a-b=c/d, a=b_c/d, a=b+c/d (3 instances)
		self.assertLuckyReasonSet('11:22', set(['1*1*2=2', '1*1=2/2', '1/1*2=2', '1/1=2/2', '1-1+2=2', '1-1=2-2', '1=1*2/2', '1=1/2*2', '1=1+2-2', '1=1-2+2']))  # format a*b*c=d, a*b=c/d, a/b*c=d, a/b=c/d, a-b+c=d, a-b=c-d, a=b*c/d, a=b/c*d, a=b+c-d, a=b-c+d (4 instances)

	def test_math_weird_reasons(self):
		# unique cases
		self.assertLuckyReasonSet('12:53', set(['1*2=5-3']))  # format a/b=c, a-b=c, a=b*c, a=b+c (1 instances)
		self.assertLuckyReasonSet('2:42', set(['2=4/2', '2=4-2']))  # format a/b=c, a-b=c, a=b*c, a=b+c (1 instances)
		self.assertLuckyReasonSet('12:43', set(['1_2/4=3', '1_2=4*3', '1-2+4=3', '1=2-4+3']))  # format a/b=c, a-b=c, a=b*c, a=b+c (1 instances)
		self.assertLuckyReasonSet('10:55', set(['1_0-5=5', '1_0=5+5', '1*0_5=5', '1*0+5=5', '1*0=5-5', '1+0=5/5', '1-0=5/5', '1=0_5/5', '1=0+5/5']))  # format a/b=c, a-b=c, a=b*c, a=b+c (1 instances)
		self.assertLuckyReasonSet('12:21', set(['1*2/2=1', '1*2=2*1', '1*2=2/1', '1/2*2=1', '1+2-2=1', '1+2=2+1', '1-2+2=1', '1=2/2*1', '1=2/2/1', '1=2-2+1']))  # format a/b=c, a-b=c, a=b*c, a=b+c (1 instances)

	def test_not_math(self):
		self.assertNotLucky('2:23')
		self.assertNotLucky('2:54')
		self.assertNotLucky('3:28')
		self.assertNotLucky('4:10')
		self.assertNotLucky('7:24')
		self.assertNotLucky('7:54')
		self.assertNotLucky('8:09')
		self.assertNotLucky('8:55')
		self.assertNotLucky('9:43')
		self.assertNotLucky('11:59')
