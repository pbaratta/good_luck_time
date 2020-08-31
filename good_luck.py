import itertools
import operator
import collections

def all_hhmm(do_24hr=False):
	' produce a generator of all (hh,mm) tuples '
	if do_24hr:
		max_hour = 24
	else:
		max_hour = 12

	return itertools.product(
		range(1, max_hour + 1),
		range(60),
	)


def find_time_tup(hhmm):
	' convert from (hh,mm) to (h?,h,m,m) '
	hour, minute = hhmm

	if hour < 10:
		# just include the one digit
		hour_digits = (hour,)
	else:
		# include both digits
		hour_digits = divmod(hour, 10)

	minute_digits = divmod(minute, 10)
	return hour_digits + minute_digits

def find_time_disp(hhmm):
	' convert from (hh,mm) to "hh:mm" string '
	hour, minute = hhmm
	return f'{hour}:{minute:02d}'

def is_same(time_tup):
	' are all the digits the same? '
	if len(set(time_tup)) == 1:
		return (True, 'repeated digit')
	else:
		return (False, None)

def pairwise(iterable):
	's -> (s0,s1), (s1,s2), (s2, s3), ...'
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)

def is_steps(time_tup):
	' are the digits incrementing/decrementing? '

	# all the differences between successive digits
	digit_diffs = [
		b - a
		for (a,b) in pairwise(time_tup)
	]

	# how many unique values?
	digit_diffs = set(digit_diffs)
	if len(digit_diffs) == 1:
		digit_diff = digit_diffs.pop()

		if digit_diff == -1:
			return (True, 'decrementing')
		elif digit_diff == 1:
			return (True, 'incrementing')
		else:
			return (False, None)

	return (False, None)

def is_palindrome(time_tup):
	' are the digits a palindrome? '
	if time_tup == time_tup[::-1]:
		return (True, 'palindrome')
	else:
		return (False, None)

def evaluate(nums, ops):
	"""take a math expression and return its value

	inputs:
		nums is a tuple of numbers to be evaluated
		ops is a tuple of operator strings to fit in between

		there must be one extra number beyond the operators
			len(nums) == len(ops) + 1

	output:
		a number if just a numerical expression (1+3/3) => 2
		a boolean if it includes an equal sign (1=2) => False	

	examples:
		(1,2,3), (+,=)		=>	1+2=3	=>	True
		(1,2,3,4), (+,*,=)	=>	1+2*3=4	=>	False
		(8,2,3), (-,+)		=>	8-2+3	=>	9
		(1,3,3), (+,/)		=>	1+3/3	=>	2
		(1,2), (=)			=>	1=2		=>	False
		(1,2,3,9), (_,=,+)	=>	12=3+9	=>	True
		(2,2,2), (=,=)		=>	2=2=2	=>	False (because 2=2 is True and True=2 is False)
	"""

	nums = list(nums)
	ops = list(ops)

	for op_set in evaluate.OP_ORDER:
		op_idx =0
		while op_idx < len(ops):
			op_str = ops[op_idx]

			if op_str in op_set:
				left = nums[op_idx]
				right = nums[op_idx + 1]
				op = evaluate.OPS[op_str]

				try:
					newval = op(left, right)
				except ZeroDivisionError as err:
					return err  # or some other value to propagate failure

				nums[op_idx:op_idx+2] = [newval]
				ops[op_idx:op_idx+1] = []
			else:
				op_idx += 1

	assert len(nums) == 1
	assert len(ops) == 0
	return nums[0]

def number_eq(a, b):
	' are a and b the same number? '
	if bool in (type(a), type(b)):
		return a is b
	else:
		return a == b

evaluate.OPS = {
	'_': (lambda a,b: 10*a+b),  # concatenate digits
	'*': operator.mul,
	'/': operator.truediv,
	'+': operator.add,
	'-': operator.sub,
	'=': number_eq,  # can't use operator.is_ or operator.eq, ah well
}

evaluate.OP_ORDER = [
	'_',
	'*/',  # if you have 6 / 2 * 3, it should be 9 not 1
	'+-',  # if you have 8 - 2 + 3, it should be 9 not 3
	'=',  # restriction that there's only 1?
]


def is_math_problem(time_tup):
	' produce all math equations from the time given or say None '
	op_gen = itertools.product(evaluate.OPS, repeat=len(time_tup)-1)
	success_eqns =[]

	for ops in op_gen:
		eqn_value = evaluate(time_tup, ops)

		if eqn_value is True:  # using == will allow truthy values, like 1
			# return True  # easy solution, terminates early

			# produce string representation
			eqn_in_order = [0] * (len(ops) + len(time_tup))
			eqn_in_order[::2] = (str(num) for num in time_tup)
			eqn_in_order[1::2] = ops
			success_eqns.append(''.join(eqn_in_order))

	if success_eqns:
		return (True, ', '.join(success_eqns))
	else:
		return (False, None)


def check_all_times(do_24hr=False):
	""" partition all times into lucky and unlucky, produce report


	"""
	checks = [
		is_same,
		is_steps,
		is_palindrome,
		is_math_problem,
	]

	lucky_table = []

	for hhmm in all_hhmm(do_24hr):
		# format the time
		time_tup = find_time_tup(hhmm)
		time_disp = find_time_disp(hhmm)

		# check all the types of luckiness
		reasons = [
			is_lucky(time_tup)
			for is_lucky in checks
		]

		# we save these reasons for later
		new_row = [time_disp, False] + reasons

		# find a unified reason
		reasons = [r for r in reasons if r is not None]
		if reasons:
			new_row[1] = True
			new_row.append(', '.join(reasons))
		else:
			new_row.append(None)

		# add the new row to the table
		lucky_table.append(new_row)

	return lucky_table

def analyze(lucky_table):
	by_col = list(zip(*lucky_table))

	lucky_count = collections.Counter(by_col[1])
	print(f'{lucky_count[True]} lucky times')
	print(f'{lucky_count[False]} unlucky times')

	same_count  = collections.Counter(by_col[2])
	same_out = 'repeated digit'
	print(f'{same_out} happened {same_count[same_out]} times')

	step_count  = collections.Counter(by_col[3])
	inc_out = 'incrementing'
	dec_out = 'decrementing'
	print(f'{inc_out} happened {step_count[inc_out]} times')
	print(f'{dec_out} happened {step_count[dec_out]} times')

	palin_count = collections.Counter(by_col[4])
	palin_out = 'palindrome'
	print(f'{palin_out} happened {palin_count[palin_out]} times')

def print_reasons(lucky_table):
	for row in lucky_table:
		time_disp = row[0]
		luckiness = row[1]
		reason = row[-1]

		if luckiness:
			print(f"{time_disp} is lucky ({reason})")
		else:
			print(f"{time_disp} is unlucky")

def print_table(lucky_table):
	for row in lucky_table:
		print("\t".join(str(val) for val in row))

def main():
	lucky_table = check_all_times()
	print_reasons(lucky_table)
	print()
	analyze(lucky_table)


if __name__ == '__main__':
	main()
