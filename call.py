"""
call.py - Telemarketing script that displays the next name 
          and phone number of a Customer to call.

          This script is used to drive promotions for 
          specific customers based on their order history.
          We only want to call customers that have placed
          an order of over 20 Watermelons.

"""
import time
from datetime import date

def get_date():
	"A function to retrieve today's date, and return string in form MM/DD/YYYY"
	datetime_date = date.today()
	year_month_day = str(datetime_date).split('-')
	today = year_month_day[1]+'/'+year_month_day[2]+'/'+year_month_day[0]
	return today

def update_csv(filename, customer_id):
	"A function to update a customer's date-called to today's date"
	today = get_date()
	f = open(filename) # make a copy of the csv file
	with open(filename, 'r+') as csvfile: # open csv file for reading/writing
		for row in f:
			row_list = row.split(',')
			if row_list[0] == customer_id: # if the customer id matches
				row_list[5]=today # update date to today's date
				row_string = '' # initialize new row string
				for item in row_list:
					if item == today:
						row_string+= str(item)+'\n' # append end of line
					else: 
						row_string+= str(item)+',' # append customer data
				csvfile.write(row_string) # write updated row
			else:
				csvfile.write(row) # else, write copy of row

# Load the customers from the passed filename
# Return a dictionary containing the customer data
#    (key = customer_id)
def load_customers(filename):
	customers = {}
	f = open(filename)

	# First line of the file should be the header, 
	# customer_id,first,last,email,telephone,called
	#   split that into a list
	header = f.readline().rstrip().split(',')

	# Process each line in a file, create a new
	#   dict for each customer
	for line in f:
		data = line.rstrip().split(',')
		customer = {}

		# Loop through each column, adding the data
		#   to the dictionary using the header keys
		for i in range(len(header)):
			customer[header[i]] = data[i] 
			# key is the header, value is the customer-specific info

		# Add the customer to our dictionary by customer id
		customers[customer['customer_id']] = customer
		# in the customers dict, customer_id is the key, customer dict is value

	# Close the file
	f.close()

	return customers # dictionary of all customers

# Load the orders from the passed filename
# Return a list of all the orders
def load_orders(filename):
	orders = []
	f = open(filename)

	# First line of the file should be the header, 
	# order_id,order_date,status,customer_id,email,address,city,state,postalcode,num_wat
	#   split that into a list
	header = f.readline().rstrip().split(',')

	# Process each line in a file, create a new
	#   dict for each order
	for line in f:
		data = line.rstrip().split(',') # split each order line

		# Create a dictionary for the order by combining
		#   the header list and the data list
		order = dict(zip(header, data)) 
		# use header & data lists to make tuples
		# first item in tuple (header) is used as dict key, data as dict value

		# Add the order to our list of orders to return
		orders.append(order)

	# Close the file
	f.close()

	return orders

def display_customer(customer):
	print "---------------------"
	print "Next Customer to call"
	print "---------------------\n"
	print "Name: ", customer.get('first', ''), customer.get('last', '')
	print "Phone: ", customer.get('telephone')
	print "\n"
	return customer.get('customer_id', '')
	# Added return value so the selected customer could be fed into update_csv()

def main():
	# Load data from our csv files
	customer_file = 'customers.csv' # added filename as variable
	customers = load_customers('customers.csv')
	orders    = load_orders('orders.csv')

	# Loop through each order
	for order in orders:
		# Is this order over 20 watermelon?
		if order.get('num_watermelons', 0) > 20:
			# Has this customer not been contacted yet?
			customer = customers.get(order.get('customer_id', 0), 0)
			if customer.get('called', '') == '':
				customer_id = display_customer(customer)
				update_csv(customer_file, customer_id) # added call to update_csv
				break 
			# loop runs until it finds a customer >20 that hasn't been called
			# shows one customer, and breaks out of for loop

if __name__ == '__main__':
	main()