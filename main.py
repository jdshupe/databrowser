#!/usr/bin/env python3
"""
Demonstration example for GitHub Project at
https://github.com/IngoMeyer441/simple-term-menu

This code only works in python3. Install per

	sudo pip3 install simple-term-menu

"""
import time
import sqlite3
from simple_term_menu import TerminalMenu
from tabulate import tabulate
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Connect to my database, this can be updated later to a different place
con = sqlite3.connect("/home/john/vimwiki/wiki.db")
cur = con.cursor()


# Search Menu and sub functions
def search_menu():
	# Setting up options for the menu
	search_menu_title = "Procurement Database/Search"
	search_menu_items = ["[p]Person", "[c]Company", "", "[q]Back to Main Menu"]
	search_menu_cursor = "> " 
	search_menu_cursor_style = ("fg_red", "bold")
	search_menu_style = ("bg_red", "fg_yellow")
	search_menu_back = False

	# Create the menu
	search_menu = TerminalMenu(
		search_menu_items,
		title=search_menu_title,
		menu_cursor=search_menu_cursor,
		menu_cursor_style=search_menu_cursor_style,
		menu_highlight_style=search_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True
	)

	# Add the logic
	while not search_menu_back:
		search_sel = search_menu.show()

		if search_sel == 0:
			search_person_menu()
		elif search_sel == 1:
			search_company_menu()
		elif search_sel == 3 or search_sel == None:
			search_menu_back = True
			print("Back Selected")

# Sub menu for searching people
def search_person_menu():
	search_person_menu_title = "Procurement Database/Search/Person"
	search_person_menu_items = ["[f]First Name", "[l]Last Name", "[p]Phone Number", "", "[q]Back to Search Menu"]
	search_person_menu_cursor = "> "
	search_person_menu_cursor_style = ("fg_red", "bold")
	search_person_menu_style = ("bg_red", "fg_yellow")
	search_person_menu_back = False

	search_person_menu = TerminalMenu(
		search_person_menu_items,
		title=search_person_menu_title,
		menu_cursor=search_person_menu_cursor,
		menu_cursor_style=search_person_menu_cursor_style,
		menu_highlight_style=search_person_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True
	)

	while not search_person_menu_back:
		search_sel = search_person_menu.show()

		if search_sel == 0:
			search_person_by_first_name(input("Lookup by First Name: "))
		elif search_sel == 1:
			search_person_by_last_name(input("Lookup by Last Name: "))
		elif search_sel == 2:
			search_person_by_cell(input("Lookup by Phone Number: "))
		elif search_sel == 4 or search_sel == None:
			search_person_menu_back = True
			print("Back Selected")

def search_person_by_first_name(first_name):
	cur.execute("SELECT personfirstname, personlastname, personcellphone FROM personnel WHERE personfirstname LIKE ?", ['%'+first_name+'%'])
	print(tabulate(cur.fetchall(), headers=["First Name","Last Name","Cell Phone"]))
	input("Press any key to continue...")
def search_person_by_last_name(last_name):
	cur.execute("SELECT personfirstname, personlastname, personcellphone FROM personnel WHERE personlastname LIKE ?", ['%'+last_name+'%'])
	print(tabulate(cur.fetchall(), headers=["First Name","Last Name","Cell Phone"]))
	input("Press any key to continue...")
def search_person_by_cell(cell):
	cur.execute("SELECT personfirstname, personlastname, personcellphone FROM personnel WHERE personcellphone LIKE ?", ['%'+cell+'%'])
	print(tabulate(cur.fetchall(), headers=["First Name","Last Name","Cell Phone"]))
	input("Press any key to continue...")

# Sub menu for searching companies
def search_company_menu():
	search_company_menu_title = "Procurement Database/Search/Company"
	search_company_menu_items = ["[n]Name", "[c]City, State", "", "[q]Back to Search Menu"]
	search_company_menu_cursor = "> "
	search_company_menu_cursor_style = ("fg_red", "bold")
	search_company_menu_style = ("bg_red", "fg_yellow")
	search_company_menu_back = False

	search_company_menu = TerminalMenu(
		search_company_menu_items,
		title=search_company_menu_title,
		menu_cursor=search_company_menu_cursor,
		menu_cursor_style=search_company_menu_cursor_style,
		menu_highlight_style=search_company_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True
	)

	while not search_company_menu_back:
		search_company_sel = search_company_menu.show()

		if search_company_sel == 0:
			search_company_name(input("Lookup by Name: "))
		elif search_company_sel == 1:
			search_company_address_city_state(input("Lookup by City, State\nCity Name: "), input("State as 2 letter code: "))
		elif search_company_sel == 3 or search_company_sel == None:
			search_company_menu_back = True
			print("Back Selected")

def search_company_name(company_name):
	cur.execute("""
		SELECT companyname, officestreetaddress, officecity, officestate, officephone 
		FROM companies 
		LEFT JOIN offices ON offices.officecompany = companies.companyid 
		WHERE NOT is_retired 
		AND companyname LIKE ? 
		LIMIT 15""", ['%'+company_name+'%'])
	print(tabulate(cur.fetchall(), headers=["Company Name", "Street Address", "City", "State", "Phone"]))
	input("Press any key to continue...")
def search_company_address_city_state(city, state):
	cur.execute("""
		SELECT companyname, officestreetaddress, officecity, officestate, officephone 
		FROM companies 
		LEFT JOIN offices ON offices.officecompany = companies.companyid 
		WHERE NOT is_retired 
		AND officecity LIKE ? 
		AND officestate LIKE ?
		LIMIT 15""", ['%'+city+'%', '%'+state+'%'])
	print(tabulate(cur.fetchall(), headers=["Company Name", "Street Address", "City", "State", "Phone"]))
	input("Press any key to continue...")


# Browse menu and sub functions
def browse_menu():
	browse_menu_title = "Procurement Database/Browse"
	browse_menu_items = ["[p]Personnel", "[c]Companies", "[o]Offices", "", "[q]Back to Main Menu"]
	browse_menu_cursor = "> "
	browse_menu_cursor_style = ("fg_red", "bold")
	browse_menu_style = ("bg_red", "fg_yellow")
	browse_menu_back = False

	browse_menu = TerminalMenu(
		browse_menu_items,
		title=browse_menu_title,
		menu_cursor=browse_menu_cursor,
		menu_cursor_style=browse_menu_cursor_style,
		menu_highlight_style=browse_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True
	)

	while not browse_menu_back:
		add_sel = browse_menu.show()

		if add_sel == 0:
			browse_personnel()
		elif add_sel == 1:
			browse_companies()
		elif add_sel == 2:
			add_office()
		elif add_sel == 4 or add_sel == None:
			browse_menu_back = True
			print("Back Selected")

# Sub menu for browsing personnel
def browse_personnel():
	# Get a list of all personnel and convert into a list for menu options
	cur.execute("""
				SELECT 
					personfirstname || ' ' || personlastname as personname,
					personjobtitle,
					"("||substr(personcellphone,1,3)||")"
					||substr(personcellphone,4,3)||"-"
					||substr(personcellphone,7,4) as cellphone,
					personemail
				FROM personnel
			 	ORDER BY personname ASC""")

	# format the data into the display string
	person_names = [ \
			"|{0:<15}\|{1:<25}\|{2:<13}\|{3:<30}\|".format(
				x[0][:15], # name (Limited to 15)
				str(x[1])[:25], # job title (Limited to 25)
				str(x[2]), # Cell Phone
				str(x[3])[:30] # email (Limited to 30)
			) for x in cur.fetchall()]
	# Add the quit option to the list of data
	person_names.extend(["", "[q]Back to Main Menu"])

	# format the title string with column titles and widths
	main_title = "Procurement Database/Browse/People\n"
	column_headers = "{0: <6}|{1:^15}|{2:^25}|{3:^13}|{4:30}|\n".format(
				"","Name","Title","Cell Phone","Email")
	divider_row = "{: <6}|{:-<15}|{:-<25}|{:-<13}|{:-<30}|".format(
					"","","","","")
	browse_menu_title = main_title + column_headers + divider_row

	browse_menu_cursor = "> "
	browse_menu_cursor_style = ("fg_red", "bold")
	browse_menu_style = ("bg_red", "fg_yellow")
	browse_menu_back = False

	browse_menu = TerminalMenu(
		person_names,
		title=browse_menu_title,
		menu_cursor=browse_menu_cursor,
		menu_cursor_style=browse_menu_cursor_style,
		menu_highlight_style=browse_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True,
		#preview_command=get_user_data,
		#preview_size=0.25,
		#preview_title="Contact information",
		show_shortcut_hints=True,
		status_bar_below_preview=True,
		show_search_hint=True
	)

	while not browse_menu_back:
		browse_sel = browse_menu.show()
	
		if browse_sel == len(person_names) - 1:
			browse_menu_back = True;

def get_user_data(user_name):
	cur.execute("""
		SELECT 
			personfirstname || ' ' || personlastname AS personname, 
			SUBSTR(personcellphone,1,3) || '-' || SUBSTR(personcellphone,4,3) || '-' || SUBSTR(personcellphone,7,4) as personphone, 
			personemail
		FROM personnel
		WHERE personname = '""" + user_name + "'")
	return tabulate(cur.fetchall(), headers=["Name", "Cell Phone","Email"])

# Get a list of all personnel and convert into a list for menu options
def browse_companies():
	cur.execute("""
				SELECT companyname
				FROM companies
			 	ORDER BY companyname ASC""")
	company_names = [x[0] for x in cur.fetchall()]
	company_names.extend(["", "[q]Back to Main Menu"])

	browse_menu_title = "Procurement Database/Browse/Compaies"
	browse_menu_cursor = "> "
	browse_menu_cursor_style = ("fg_red", "bold")
	browse_menu_style = ("bg_red", "fg_yellow")
	browse_menu_back = False

	browse_menu = TerminalMenu(
		company_names,
		title=browse_menu_title,
		menu_cursor=browse_menu_cursor,
		menu_cursor_style=browse_menu_cursor_style,
		menu_highlight_style=browse_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True,
		preview_command=get_company_data,
		preview_size=0.25,
		preview_title="Company information",
		show_shortcut_hints=True,
		status_bar_below_preview=True,
		show_search_hint=True
	)

	while not browse_menu_back:
		browse_sel = browse_menu.show()
	
		if browse_sel == len(company_names) - 1:
			browse_menu_back = True;

# Get a list of companies matching the company_name
def get_company_data(company_name):
	offices_query = """
		SELECT
			officestreetaddress,
			officecity || ', ' || officestate as officecitystate,
			officezipcode,
			SUBSTR(officephone,1,3)||'-'||SUBSTR(officephone,4,3)||'-'||SUBSTR(officephone,7,4) as officephonenumber
		FROM
			offices
		WHERE
			officecompany = (
				SELECT
					companyid
				FROM
					companies
				WHERE
					companyname = :companyname)
	"""
	values = ({
		'companyname': company_name
		})
	cur.execute(offices_query, values)
	return tabulate(cur.fetchall(), headers=["Street Address", "City, State",
	"Zip Code", "Company Name"])


# Add menu and sub functions
def add_menu():
	add_menu_title = "Procurement Database/Add"
	add_menu_items = ["[p]Person", "[c]Company", "[o]Office", "[j]Job", "", "[q]Back to Main Menu"]
	add_menu_cursor = "> "
	add_menu_cursor_style = ("fg_red", "bold")
	add_menu_style = ("bg_red", "fg_yellow")
	add_menu_back = False

	add_menu = TerminalMenu(
		add_menu_items,
		title=add_menu_title,
		menu_cursor=add_menu_cursor,
		menu_cursor_style=add_menu_cursor_style,
		menu_highlight_style=add_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True
	)

	while not add_menu_back:
		add_sel = add_menu.show()

		if add_sel == 0:
			add_person()
		elif add_sel == 1:
			add_company()
		elif add_sel == 2:
			add_office()
		elif add_sel == 3:
			add_job()
		elif add_sel == 5 or add_sel == None:
			add_menu_back = True
			print("Back Selected")

def add_person():
	print("Procurement Database/Add/Person")
	confirmed = False
	while not confirmed:
		first_name = input("First Name? ")
		last_name = input("Last Name? ")
		
		# Check to see if there are any records matching the name
		cur.execute("SELECT * FROM personnel WHERE personfirstname LIKE ? AND personlastname LIKE ?", [first_name, last_name])
		# checks to see if any where returned
		if cur.fetchall():
			print("A record already exists for this person, are you sure you want to add?: ")
			check_value = input("y/n ")
			if check_value == "n":
				return # breaks is the user types 'n'

		cell_phone = input("Cell Phone? ")
		email = input("Email Address? ")

		# final check to make sure all info was added correctly and gives a chance to cancel.
		print("Do you want to add {} {}\ncell phone: {}\nemail: {}\nto the database?".format(first_name, last_name, cell_phone, email))
		check_value = input("y/n ")
		if check_value == "y":
			confirmed = True
		elif check_value == "n":
			return
		else:
			return
	cur.execute("INSERT INTO personnel(personfirstname, personlastname, personcellphone, personemail) VALUES(?,?,?,?)", [first_name, last_name, cell_phone, email])
	con.commit()
def add_company():
	print("Procurement Database/Add/Company")
	confirmed = False
	while not confirmed:
		company_name = input("Company Name? ")
		
		# Check to see if there are any records matching the name
		cur.execute("SELECT * FROM companies WHERE companyname LIKE ?", [company_name])
		# checks to see if any where returned
		if cur.fetchall():
			print("A record already exists for this company, are you sure you want to add?: ")
			check_value = input("y/n ")
			if check_value == "n":
				return # breaks is the user types 'n'

		# final check to make sure all info was added correctly and gives a chance to cancel.
		print("Do you want to add {} to the database?".format(company_name))
		check_value = input("y/n ")
		if check_value == "y":
			confirmed = True
		elif check_value == "n":
			return
		else:
			return
	cur.execute("INSERT INTO companies(companyname, is_retired) VALUES(?,0)", [company_name])
	con.commit()
def add_office():
	print("Procurement Database/Add/Office")
	confirmed = False
	# Get a list of existing companies to select from
	cur.execute("SELECT companyname FROM companies WHERE NOT is_retired")
	company_names = [x[0] for x in cur.fetchall()]
	completer = WordCompleter(company_names)	

	while not confirmed:
		# Get compound id fields to be able to check for duplicates
		company_name = prompt("Company Name? ", completer=completer)
		street_address = input("Street Address? ")
		
		# Check to see if there are any records matching the name
		cur.execute("SELECT * FROM offices WHERE officestreetaddress LIKE ? AND officecompany = (SELECT companyid FROM companies WHERE companyname = ?)", [street_address, company_name])
		# checks to see if any where returned
		if cur.fetchall():
			print("A record already exists for this office, are you sure you want to add?: ")
			check_value = input("y/n ")
			if check_value == "n":
				return # breaks is the user types 'n'

		city = input("City? ")
		state = input("State? (As 2 letter code) ")
		phone = input("Phone? ")
		# final check to make sure all info was added correctly and gives a chance to cancel.
		print("Do you want to add {} {} to the database?".format(company_name, street_address))
		check_value = input("y/n ")
		if check_value == "y":
			confirmed = True
		elif check_value == "n":
			return
		else:
			return
	cur.execute("INSERT INTO offices(officestreetaddress, officecity, officestate, officephone, officecompany) VALUES(?,?,?,?, (SELECT companyid FROM companies WHERE companyname = ?))", [street_address, city, state, phone, company_name])
	con.commit()
def add_job():
	print("Procurement Database/Add/Job")
	confirmed = False
	while not confirmed:
		job_name = input("Job Name? ")
		job_number = input("Job number? ")
		
		# Check to see if there are any records matching the name
		cur.execute("SELECT * FROM jobs WHERE jobnumber LIKE ?", [job_number])
		# checks to see if any where returned
		if cur.fetchall():
			print("A record already exists for this job, are you sure you want to add?: ")
			check_value = input("y/n ")
			if check_value == "n":
				return # breaks is the user types 'n'

		street_address = input("Street Address? ")
		city = input("City? ")
		state = input("State? ")

		# final check to make sure all info was added correctly and gives a chance to cancel.
		print(('Do you want to add {} - {}\n'
				'Street Address: {}\n'
				'City, State: {}, {}\n'
				'to the database?' ) \
			.format(job_number, job_name, street_address, city, state))
		check_value = input("y/n ")
		if check_value == "y":
			confirmed = True
		elif check_value == "n":
			return
		else:
			return
	cur.execute("INSERT INTO jobs(jobname, jobnumber, jobstreetaddress, city, \
			 state ) VALUES(?,?,?,?,?)", [job_name, job_number, street_address, \
								 city, state])
	con.commit()

# Build main menu
def main():
	main_menu_title = "Procurement Database/Main Menu"
	main_menu_items = ["[s]Search", "[a] Add", "[u]Update Entry", "[b]Browse", "", "[q]Quit"]
	main_menu_cursor = "> "
	main_menu_cursor_style = ("fg_red", "bold")
	main_menu_style = ("bg_red", "fg_yellow")
	main_menu_exit = False

	main_menu = TerminalMenu(
		menu_entries=main_menu_items,
		title=main_menu_title,
		menu_cursor=main_menu_cursor,
		menu_cursor_style=main_menu_cursor_style,
		menu_highlight_style=main_menu_style,
		cycle_cursor=True,
		clear_screen=True,
		skip_empty_entries=True,
	)


	while not main_menu_exit:
		main_sel = main_menu.show()

		if main_sel == 0:
			search_menu()
		elif main_sel == 1:
			add_menu()
		elif main_sel == 2:
			print("option 3 selected")
			time.sleep(5)
		elif main_sel == 3:
			browse_menu()
		elif main_sel == 5 or main_sel == None:
			main_menu_exit = True
			con.close()
			print("Quit Selected")


# Main Loop
if __name__ == "__main__":
	main()
