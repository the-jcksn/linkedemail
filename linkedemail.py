import pandas as pd
print("[!] Instructions for use:\n")
print("[1] Log into LinkedIn in your browser and navigate to the company's main page.")
print("[2] Click on the 'people' tab and scroll ALL the way to the bottom, until it loads no more staff.")
print("[3] Once at the bottom, right-click and 'save page as', save this in the same directory as this script.")
print("[4] Delete any folders this downloaded, we are only after the page's code.")
print("[5] It may be useful to rename the code file as something easy, such as 'index.html' .")
instructions = input("\n[!] Are these initial tasks complete? (y/n): ")
while instructions != "y" and instructions != "n":
	print("[!] Invalid selection: Please try again")
	instructions = input("\n[!]Are these initial tasks complete? (y/n): ")
if instructions == "n":
	print("[+] Please perform the prep first and then return.")
	print("[+] Goodbye.")
	quit()

filename = input("[+] Please enter the filename that was saved: ")
file = open(filename, "r")
users_url = []
user_noinverts = []
poss_usernames = []
user_dupes = []
user_final = []
email_names = []
email_address = []
for line in file:
	if "https://www.linkedin.com/in/" in line:
		users_url.append(line)
for line in users_url:
	count = 0
	position_start = 0
	position_end = 0
	for char in line:
		if count < 4:
			if char == "/":
				count += 1
			position_start += 1
			position_end += 1
		elif count < 5:
			if char == "/":
				count += 1
			position_end += 1
	newline = line[position_start:position_end]
	poss_usernames.append(newline)
for line in poss_usernames:
	count = 0
	position_end = 0
	for char in line:
		if count < 2:
			if char == "-":
				count += 1
			position_end += 1
	newuser = line[0:position_end-1]
	user_dupes.append(newuser)
for users in user_dupes:
	count = 0
	position_end = 0
	if "\"" in users:
		for char in users:
			if count < 1:
				if char == "\"":
					count += 1
				position_end += 1
			userstripped = users[0:position_end-1]
	else:
		userstripped = users
	if userstripped not in user_noinverts:
		user_noinverts.append(userstripped)
for person in user_noinverts:
	count = 0
	position_end = 0
	if "?" in person:
		for char in person:
			if count < 1:
				if char == "?":
					count += 1
				position_end += 1
		userfinal = person[0:position_end-1]
	else:
		userfinal = person
	user_final.append(userfinal)
for i in user_final:
	with open("usernames.txt", "a") as f:
		f.write(i)
		f.write("\n")
print("\n[!] ",len(user_final), "usernames found! - saved as 'usernames.txt'")
print("\n[?] Some of these usernames are in the format 'firstname-lastname' - would you like to convert these to email addresses?")
yesno = input("[?] Please choose y/n: ")
while yesno != "y" and yesno != "n":
	yesno = input("[?] Please choose y/n: ")
if yesno == "n":
	print("\n [+] Goodbye.")
	quit()
for name in user_final:
	if "-" in name:
		nodashname = name.replace("-",".")
		email_names.append(nodashname)
domain = input("[?] Please enter the domain to append after 'first.last@': ")
for firstlast in email_names:
	address = firstlast + "@" + domain
	email_address.append(address)
for emailadd in email_address:
	with open("emails.txt", "a") as output:
		output.write(emailadd)
		output.write("\n")
print("\n[!] ", len(email_address), "email addresses created! - saved as emails.txt")
print("\n[?] Would you like to create a csv file (suitable for use with excel?)")
csvfile = input("[+] Please choose y/n: ")
while csvfile != "y" and csvfile != "n":
	csvfile = input("[+] Please choose y/n: ")
if csvfile == "n":
	print("\n [+] Goodbye.")
	quit()
firstname = ["first name"]
lastname = ["last name"]
email = ["email"]
for human in email_address:
	firstdot = 0
	firstend = 0
	firstat = 0
	lastend = 0
	for char in human:
		if firstdot < 1:
			if char == ".":
					firstdot += 1
			firstend += 1
		if firstat < 1:
			if char == "@":
					firstat += 1
			lastend += 1
	first_name = human[0:firstend-1]
	firstname.append(first_name)
	last_name = human[firstend:lastend-1]
	lastname.append(last_name)
	email.append(human)
df = pd.DataFrame(list(zip(*[firstname, lastname, email])))
df.to_csv("staff.csv", index=False)
print("\n[+] Data written to 'staff.csv'")

print("[+] Goodbye")
