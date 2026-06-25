#!/usr/bin/env python3
import os
import sys
from ezclear import cls
from pathlib import Path
from datetime import datetime

VERSION = "v1.9"
LOGO = r""":::::::::      :::   :::   :::  ::::::::      :::     :::     ::: :::::::::: :::::::::
 :+:    :+:   :+: :+: :+:   :+: :+:    :+:   :+: :+:   :+:     :+: :+:        :+:    :+:
  +:+    +:+  +:+   +:+ +:+ +:+  +:+         +:+   +:+  +:+     +:+ +:+        +:+    +:+
   +#+    +:+ +#++:++#++: +#++:   +#++:++#++ +#++:++#++: +#+     +:+ +#++:++#   +#++:++#:
    +#+    +#+ +#+     +#+  +#+           +#+ +#+     +#+  +#+   +#+  +#+        +#+    +#+
     #+#    #+# #+#     #+#  #+#    #+#    #+# #+#     #+#   #+#+#+#   #+#        #+#    #+#
      #########  ###     ###  ###     ########  ###     ###     ###     ########## ###    ###"""

def get_save_file() -> Path:
	# Get cross-platform save file path
	home = Path.home()

	if os.name == 'nt':  # Windows
		data_dir = home / 'AppData' / 'Local' / 'daysaver'
	elif sys.platform == 'darwin':  # macOS
		data_dir = home / 'Library' / 'Application Support' / 'daysaver'
	else:  # Linux and others
		data_dir = home / '.local' / 'share' / 'daysaver'

	data_dir.mkdir(parents=True, exist_ok=True)
	return data_dir / 'save'

def load_dates() -> list[str]:
	# Load dates from file, return as list of stripped lines
	file_path = get_save_file()
	if not file_path.exists():
		return []
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			return [line.strip() for line in f if line.strip()]
	except Exception as e:
		print(f"Error loading file: {e}")
		return []

def save_dates(dates: list[str]):
	# Save list of dates to file
	file_path = get_save_file()
	try:
		with open(file_path, 'w', encoding='utf-8') as f:
			f.write('\n'.join(dates) + '\n' if dates else '')
	except Exception as e:
		print(f"Error saving file: {e}")

def parse_search_filters(query: str) -> dict:
	"""Parse search query into filters: y, m, d, or legacy string search."""
	filters = {'y': None, 'm': None, 'd': None, 'legacy': None}
	parts = query.strip().lower().split()

	if not parts:
		return filters

	# Check if it looks like legacy date or partial string
	if any('.' in p for p in parts) or len(parts) == 1 and (parts[0].count('.') == 2 or not any(k in parts[0] for k in (':', 'y', 'm', 'd'))):
		filters['legacy'] = query.strip()
		return filters

	# Parse filters like y:2026 m:06 d:25 or m:6
	for part in parts:
		if ':' in part:
			key, val = part.split(':', 1)
			key = key.strip().lower()
			val = val.strip()
			if key in ('y', 'year'):
				filters['y'] = val
			elif key in ('m', 'month'):
				filters['m'] = val.zfill(2) if val.isdigit() and len(val) == 1 else val
			elif key in ('d', 'day'):
				filters['d'] = val.zfill(2) if val.isdigit() and len(val) == 1 else val
		else:
			# Single number: infer context
			if val := part.strip():
				if val.isdigit():
					num = int(val)
					if 1 <= num <= 12:
						filters['m'] = val.zfill(2)
					elif 13 <= num <= 31:
						filters['d'] = val.zfill(2)
					else:
						filters['y'] = val
				else:
					filters['legacy'] = val
	return filters

def matches_filters(date: str, filters: dict) -> bool:
	"""Check if date matches the filters."""
	if filters['legacy']:
		return filters['legacy'] in date

	parts = date.split('.')
	if len(parts) != 3:
		return False
	y, m, d = parts

	match = True
	if filters['y'] and filters['y'] != y:
		match = False
	if filters['m'] and filters['m'] != m:
		match = False
	if filters['d'] and filters['d'] != d:
		match = False
	return match

def help_command():
	print("Commands:")
	print("  l             List all saved dates")
	print("  a YYYY.MM.DD  Add a new date")
	print("  r YYYY.MM.DD  Remove a date")
	print("  s [filters]   Search for dates (see below)")
	print("  h             Show this help")
	print("  q             Quit")
	print("  c             Clear screen")
	print("  t             Add today to saved dates")
	print("\nDates are stored in YYYY.MM.DD format, one per line.")
	print(f"Default save file location is {get_save_file()}")
	print("Autosave is enabled (cannot be disabled)")
	print("\nSearch examples:")
	print("  s 2026.06.25          Legacy exact/partial search")
	print("  s m:06 d:25 y:2026    Month 06, day 25, year 2026")
	print("  s d:12                All dates with day 12")
	print("  s m:6                 All dates in June (any year/day)")
	print("  s 6                   Single number: prefers month, then day, then year")
	print("  s y:2025              All dates in 2025")
	print("At least one filter/keyword required.")

def main():
	cls()
	print(VERSION)
	print(f"{LOGO}\n")
	print("Welcome to Daysaver! Type 'h' for help.\n")
	while True:
		try:
			user_input = input("\n> ").strip().lower()

			if not user_input:
				continue

			parts = user_input.split(maxsplit=1)
			cmd = parts[0]

			if cmd == 'q' or cmd == 'quit' or cmd == 'exit' or cmd == 'leave':
				print("Goodbye!")
				break

			elif cmd == 'l':
				dates = load_dates()
				if dates:
					print("\nSaved dates:")
					print("      YYYY.MM.DD")
					for i, date in enumerate(dates, 1):
						print(f"  {i:2d}. {date}")
				else:
					print("No dates saved yet.")

			elif cmd == 'h':
				help_command()

			elif cmd == 'c' or cmd == 'clear' or cmd == 'cls':
				cls()

			elif cmd in ('a', 'r', 's'):
				if len(parts) < 2:
					print(f"Usage: {cmd} YYYY.MM.DD or filters")
					continue

				query = parts[1].strip()

				dates = load_dates()

				if cmd == 'a':
					# Basic validation
					if not query.count('.') == 2 or len(query) != 10:
						print("Date should be in YYYY.MM.DD format")
						continue
					if query in dates:
						print(f"Date {query} already exists.")
					else:
						dates.append(query)
						dates.sort()
						save_dates(dates)
						print(f"Added {query}")

				elif cmd == 'r':
					if query in dates:
						dates.remove(query)
						save_dates(dates)
						print(f"Removed {query}")
					else:
						print(f"Date {query} not found.")

				elif cmd == 's':
					filters = parse_search_filters(query)
					matches = [d for d in dates if matches_filters(d, filters)]

					if matches:
						print(f"\nFound {len(matches)} matching date(s):")
						for m in matches:
							print(f"  {m}")
					else:
						print("No matches found.")

			elif cmd == 't':
				now = datetime.now()
				date_str = f"{now.year}.{now.month:02d}.{now.day:02d}"
				dates = load_dates()

				if date_str in dates:
					print(f"Date {date_str} already exists.")
				else:
					dates.append(date_str)
					dates.sort()
					print(f"Added today's date: {date_str}!")
					save_dates(dates)

			else:
				print("Invalid command. Type 'h' for help.")

		except KeyboardInterrupt:
			print("\nGoodbye!")
			break
		except Exception as e:
			print(f"ERROR: {e}")

if __name__ == "__main__":
	main()
