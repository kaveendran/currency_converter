
from flask import Flask,render_template,request,flash,session
import sqlite3
import requests
# from flask_session import Session




API= "NCBIFMP7K04TYN59"

	
global login_stat
login_stat = False




app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


	




# handle login 
@app.route('/',methods=["POST","GET"])

def login():
	
	# call database for get  password and
	if request.method == "GET":
		return render_template("login.html")
	elif request.method == "POST":
		# extract data from http request
		
		name = request.form.get("name")
		password =request.form.get("password")




		# handling inputs 
		if not(name):
			msg = "Name field empty!"
			return render_template("login.html",message = msg)
			# return "name cant be empty"
		elif not(password):
			msg= "password cant be empty"
			return render_template("login.html",message = msg)
		else:
			conn = sqlite3.connect("database.db")			
			cur = conn.cursor()
			cur.execute("SELECT password FROM data WHERE name ='{}'".format(name))
			data = cur.fetchall()
			conn.close()
			print(data)
			# print(type(data[0][0]))
			print(type(password))

			try:
				data_get =data[0][0]

			except:
				data_get = 0
			
			# error hadling 
			
			if data_get == 0:
				print("No match.......")
				msg ="password or name not match"				
				return render_template("login.html",message = msg)
			
			elif password == str(data_get):

				print("password match")

				global login_stat
				
				login_stat = True
				print(login_stat)
				return render_template("home.html")

			else:
				print("Password not match")
				msg ="password not match"				
				return render_template("login.html",message = msg)

				
			
			
				
	




@app.route('/next',methods=["POST","GET"])
def start():
	print(login_stat)
	
		
	if request.method == "POST":
		# extract data from http post request
		c_from = request.form.get("from")
		c_to = request.form.get("to")
		c_amount = request.form.get("amount")
		# handling empty inputs
		if not(c_amount):
			c_amount = '0'

		print("nothing inputed: {}".format(c_amount))

		
		# c_amount = int(c_amount)
		# test = c_from + c_to + c_amount
		try:
			c_amount_int = float(c_amount)
		except:
			print("value error")
		

		#===================================================== API INTEGRATION =========================
		# sort same currency selection
		if c_from == c_to:
			msg ="Same Currency selected"
			return render_template("converter.html",show=msg)
		# sort zero input and empty field
		elif c_amount_int <= 0:
			z_m_error = "Invalid Input"
			return render_template("converter.html",show=z_m_error)
		elif c_amount == "":
			empty = "Input Cant be empty"		
		else:

			url = 'https://v6.exchangerate-api.com/v6/78755d6c233558e5e0815a5f/latest/{}'.format(c_from)
			r = requests.get(url)
			data = r.json()

			print(data)

			# amount * 5. Exchange Rate = amount
			E_rate = data["conversion_rates"]["{}".format(c_to)]
			
			print(E_rate)
			E_rate_c = float(E_rate)
			C_amount = E_rate_c * c_amount_int
			C_amount = round(C_amount,2)
			print("Amount{}".format(C_amount))
			print_text ="{} To {}  Amount {}{}".format(c_from,c_to,C_amount,c_to)
			return render_template("converter.html",show=print_text)
	else:
		return render_template("converter.html")


# main driver function
if __name__ == '__main__':


	app.run(debug=True)



# created login status so we can track that user is logined or not  for that  need to implement code ???????????
	