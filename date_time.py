import datetime

def date_time(date_time: datetime):
	"""
	Returns formated date time from datetime class
	:param date_time:
	:return:
	"""
	datetime_obj = date_time
	# Extract year, month, day
	year = datetime_obj.year
	month = datetime_obj.month
	day = datetime_obj.day
	hour = datetime_obj.hour
	minute = datetime_obj.minute

	# Get the full name of the weekday
	weekday_name = datetime_obj.strftime('%A')
	# print(f"Year: {year}")
	# print(f"Month: {month}")
	# print(f"Day: {day}")
	# print(f"Weekday (name): {weekday_name}")
	# print(f'Hour {hour}')
	# print(f'Minute {minute}')
	formatted_date = f'{year}-{month}-{day} {weekday_name} {hour}:{minute}'
	return formatted_date

def main():
	""" to run the script"""
	day = datetime.datetime.now()
	date_time(day)

if __name__ == "__main__":
	main()