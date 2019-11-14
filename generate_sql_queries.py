'''
About this script -
* The dictionary 'source' will be used to maintain the data of the tables that need to be compared.
* Please make sure the number of columns in Table A is equal to those in Table B.
* I have a check for the same so you don't have to worry. :3 (But just to avoid working again on the same thing)
* Please make sure the primary column name exists in the corresponding table columns or else an error prompt will be shown.
* Also, number of columns can be n where n is the maximum number of columns that your laptop can bear while loading the data into the tables. As far as my code is concerned, it will generate the scripts you need.
* n can be any number, it doesn't have to be just 3.
* The table columns need to be in the right order for the script to be able to generate the correct queries.
* Note - Please make sure the column mapping is correct.
* Table A - Table for Application Data
* Table B - Table for Business Data
'''

# --------------------------------------------------------------
# Import Section
import json
# End of Import Section
# --------------------------------------------------------------

# --------------------------------------------------------------
# Source Data Section
# Template Source for Table Name and Table Column values for the two tables to be compared

# IMPORTANT NOTE -
# table_A -> Application Data
# table_B -> Business Data

source = {
	'table_A': 'Table_A',
	'table_B': 'Table_B',
	'table_A_primary': 'col_A1',
	'table_A_columns': ['col_A1', 'col_A2', 'col_A3', 'col_A4', 'col_A5'],
	'table_B_primary': 'col_B1',
	'table_B_columns': ['col_B1', 'col_B2', 'col_B3', 'col_B4', 'col_B5']
}

# Let's see how this looks in the console
print(json.dumps(source, indent=4))

# End of Source Data Section
# --------------------------------------------------------------

# --------------------------------------------------------------
# Function Definitions

# Definition of the function precheck
# This function will check if -
# 1. Both the tables have some table name (non empty table names)
# 2. Both the tables have non empty column names
# 3. Both the primary columns are present in the list of corresponding table column array list
# 4. Number of columns in both the tables are equal 

def precheck():
	print('Precheck log(s) -')

	# Table Name Check
	table_A_name_check = source['table_A']
	if not table_A_name_check:
		print('Table A name is empty')

	table_B_name_check = source['table_B']
	if not table_B_name_check:
		print('Table B name is empty')


	# Column Name Check
	table_A_column_check = all(source['table_A_columns'])
	if not table_A_column_check:
		print('Table A has empty column(s)')
		return False

	table_B_column_check = all(source['table_B_columns'])
	if not table_B_column_check:
		print('Table B has empty column(s)')
		return False	


	# Check if Primary keys exist in corresponding tables
	primary_check_tableA = (source['table_A_primary'] in source['table_A_columns'])
	if not primary_check_tableA:
		print("Primary key of Table A is either empty or doesn't exist in Table A Columns")
		return False

	primary_check_tableB = (source['table_B_primary'] in source['table_B_columns'])
	if not primary_check_tableB:
		print("Primary key of Table B is either empty or doesn't exist in Table B Columns")		
		return False


	# Check if number of columns in both the tables are the same
	column_count_check = ( len(source['table_A_columns']) == len(source['table_B_columns']) )
	if not column_count_check:
		print("Number of columns in both the tables don't match")
		return False

	# Return the precheck status
	return (table_A_name_check and table_B_name_check and table_A_column_check and table_B_column_check and primary_check_tableA and primary_check_tableB and column_count_check)

# End of the function definition
# --------------------------------------------------------------


# Definition of the function query_count_primary
def query_count_primary():	
	return "SELECT COUNT(*) FROM " + source['table_B'] +  " B \nWHERE EXISTS (\n\tSELECT * FROM " + source['table_A'] + " A\n\tWHERE B." + source['table_B_primary'] + " = A." + source['table_A_primary'] + "\n);"

# End of the function definition
# --------------------------------------------------------------

def count_match(b_col, a_col):
	return "SELECT COUNT(*) FROM " + source['table_B'] +  " B \nWHERE EXISTS (\n\tSELECT * FROM " + source['table_A'] + " A\n\tWHERE B." + source['table_B_primary'] + " = A." + source['table_A_primary'] + "\n\tAND B." + b_col + " = A." + a_col + "\n);"

def count_mismatch(b_col, a_col):
	return "SELECT COUNT(*) FROM " + source['table_B'] +  " B \nWHERE NOT EXISTS (\n\tSELECT * FROM " + source['table_A'] + " A\n\tWHERE B." + source['table_B_primary'] + " = A." + source['table_A_primary'] + "\n\tAND B." + b_col + " = A." + a_col + "\n);" 

def display_mismatch(b_col, a_col):
	return "SELECT * FROM " + source['table_B'] +  " B \nWHERE NOT EXISTS (\n\tSELECT * FROM " + source['table_A'] + " A\n\tWHERE B." + source['table_B_primary'] + " = A." + source['table_A_primary'] + "\n\tAND B." + b_col + " = A." + a_col + "\n);" 

# Definition of the function generate_queries
def generate_queries():
	print("\n-- The query below will print the count of records having primary key matched from Business Data (" + source['table_B'] + ") in Application Data (" + source['table_A'] + ")\n")
	print(query_count_primary()) # call of the function query_count_primary
	print("\n")
	no_of_columns = len(source['table_A_columns'])
	for i in range(0, no_of_columns):
		if source['table_B_columns'][i] == source['table_B_primary']:
			continue
		
		print("--Comparison of " + source['table_B_columns'][i] + " with " + source['table_A_columns'][i] + "\n")

		print("--Number of matches for column " + source['table_B_columns'][i] + " with " + source['table_A_columns'][i] + " -")
		print(count_match(source['table_B_columns'][i], source['table_A_columns'][i])) # call of the function count_match
		print("\n")

		print("--Number of mismatches for column " + source['table_B_columns'][i] + " with " + source['table_A_columns'][i] + " -")
		print(count_mismatch(source['table_B_columns'][i], source['table_A_columns'][i])) # call of the function count_mismatch
		print("\n")

		print("--Display record mismatches for column " + source['table_B_columns'][i] + " with " + source['table_A_columns'][i] + " -")
		print(display_mismatch(source['table_B_columns'][i], source['table_A_columns'][i])) # call of the function display mismatch
		print("\n")

# End of generate_queries

# End of the function definition
# --------------------------------------------------------------


# Definition of the main function
def main():
	precheck_status = precheck() # call of the function precheck
	if not precheck_status:
		print('Precheck Status: Precheck failed, please read the above log to rectify the source data.')
	else:
		print('Precheck Status: Precheck passed!')
		print('Start copying SQL queries generated from here onwards -')
		generate_queries() # call fo the function generate_queries

# End of the function definition
# --------------------------------------------------------------


# End of all function definitions
# --------------------------------------------------------------

# Main Script
main() # Call of the main function