
from flask import Flask,render_template,request,flash,session,redirect,url_for
import sqlite3
import requests
from datetime import datetime
# from flask_session import Session
API= "NCBIFMP7K04TYN59"	
global login_stat
login_stat = False

app = Flask(__name__)
app.secret_key = "kaveendran"

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
			
			flash("name is empty!")
			# return render_template("login.html")
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

				# for manage sessions update user name 
				session["user"] = name
				print(session["user"])

				global login_stat
				
				login_stat = True
				print(login_stat)
				# update sessions
				# session['log'] = True
				# session['name'] = name
				# session['id'] = 1234
				return render_template("home.html")

			else:
				print("Password not match")
				msg ="password not match"				
				return render_template("login.html",message = msg)


# registration handling 
@app.route("/reg",methods=["POST","GET"])

def register():
	if request.method == "POST":
		# extracting data from requests 
		name = request.form.get("name")
		password = request.form.get("password")
		password_confirm = request.form.get("password_confirm")

		
		

		# confirming name is not already available in database
		conn = sqlite3.connect("database.db")			
		cur = conn.cursor()
		cur.execute("SELECT password FROM data WHERE name ='{}'".format(name))
		data = cur.fetchall()
		conn.close()

		if data:
			msg = "Name already taken"
			flash("{}".format(msg))
			return render_template("register.html")
		
		elif password == password_confirm:
			# update data to data base 
			conn = sqlite3.connect("database.db")
			cur = conn.cursor()
			cur.execute("INSERT INTO data(name,password) VALUES('{}','{}')".format(name,password_confirm))
			conn.commit()
			conn.close()

			return redirect(url_for("login"))

		else:
			msg = "password didnt match"
			flash("{}".format(msg))
			return render_template("register.html")
	else:
		return "Not allowed"

# initializing register form 
@app.route("/r",methods=["POST","GET"])
def reg_pass():
	if request.method == "POST":
		return render_template("register.html")
	else:
		return "404"
	

""" 
registration  added function ====== ok
hashing =========================== no
http injection ==================== ok
successfull registration redirected to login page ====== ok
need to test empty spaces

"""
# home function 
# for redirect things 

@app.route("/home",methods =["POST","GET"])
def home_red():
	if request.method == "POST":
		return render_template("home.html")
	else:
		return render_template("home.html")





# logout 
@app.route("/logout",methods=["POST"])
def logout():
	session.pop("user",None)
	print(session)
	return redirect(url_for("login"))


@app.route("/home1")
def home1():
	return redirect(url_for("home_red"))







# prevention from http get injection
@app.route("/home")
def home():
	if 'log' in session:
		return render_template("home.html")
	return redirect(url_for("login"))
	

# handle post method for currency convereter
@app.route('/next',methods=["POST","GET"])
def start():		
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

			# try to store conversion on data base 
			name = session["user"]
			now = datetime.now()
			conv= f"CURRENCY - CURRENCY {c_amount} {c_from} TO {c_to} =====> IS {C_amount} {c_to}"
			conn = sqlite3.connect("database.db")
			cur = conn.cursor()
			cur.execute("INSERT INTO conv('name','conerter','time') VALUES('{}','{}','{}')".format(name,conv,now))
			conn.commit()
			conn.close()
			print("currency conversion data inserted into dtabase")

			return render_template("converter.html",show=print_text)
	
	else:
		return redirect(url_for("login"))

# handle currency converter page 
@app.route("/next_GET",methods=["POST","GET"])
def page_post():
	if request.method == "POST":

		return render_template("converter.html")
	else:
		return redirect(url_for("login"))


# crypto to  currency converter page 
@app.route("/crypto_p",methods=["POST","GET"])

def crypt_conv():
	if request.method == "POST":
		crypto_code = request.form.get("crypto")
		money_code = request.form.get("money")
		amount = request.form.get("amount")

		if (not amount) and (not crypto_code) and (not money_code):
			msg = "Empty Fields!"
			return render_template("crypto.html",show = msg)
			
		else:
			url = "https://rest.coinapi.io/v1/exchangerate/{}/{}".format(crypto_code,money_code)
			header = {"X-CoinAPI-Key": "AD8095AA-F9DA-42CB-B4C4-FAAB69202FF6"}
			data = requests.get(url,headers=header).json()
			try:
				rate = data["rate"]
				base = data["asset_id_base"]
				quote = data["asset_id_quote"]
				new_rate = round(rate,2)
				msg = "Convertion from {} to {} is {},{}".format(base,quote,new_rate,quote)

				# store crypto to currency conversion data on data base
				name = session["user"]
				now = datetime.now()
				conv= f"CRYPTO TO CURRENCY -{amount}{base} TO  {quote} =====> IS {new_rate} {quote}"
				conn = sqlite3.connect("database.db")
				cur = conn.cursor()
				cur.execute("INSERT INTO conv('name','conerter','time') VALUES('{}','{}','{}')".format(name,conv,now))
				conn.commit()
				conn.close()
				print("currency conversion data inserted into database")

				

				return render_template("crypto.html",show = msg )
			except:
				msg = "ERROR!"
				return render_template("crypto.html",show = msg)		
	else:
		return redirect(url_for("login"))

# handle crypto converter by get req security 	
@app.route("/crypto_get",methods =["POST","GET"])
def crypto_get():

	if request.method == "POST":
		return render_template("crypto.html")
	else:
		return redirect(url_for("login"))
# ============================================================================================ tested ok


# crypto to crypto conversion and security

@app.route("/crypto_c",methods=["POST","GET"])
def crypto_cry():
	if request.method == "POST":

		return render_template("crypto_nex.html")
	else:
		return redirect(url_for("login"))


@app.route("/crypto_to_c",methods =["POST","GET"])
def crypto_crypto():
	if request.method == "POST":
		crypto_code = request.form.get("crypto")
		money_code = request.form.get("money")
		amount = request.form.get("amount")

		if (not amount) and (not crypto_code) and (not money_code):
			msg = "Empty Fields!"
			return render_template("crypto_nex.html",show = msg)
			
		else:
			url = "https://rest.coinapi.io/v1/exchangerate/{}/{}".format(crypto_code,money_code)
			header = {"X-CoinAPI-Key": "8B47736C-CC95-418E-96ED-3658B3A2672C"}
			data = requests.get(url,headers=header).json()
			try:
				rate = data["rate"]
				base = data["asset_id_base"]
				quote = data["asset_id_quote"]
				new_rate = round(rate,2)
				msg = "Convertion from {} {} to {} is {},{}".format(amount,base,quote,new_rate,quote)
				name = session["user"]
				now = datetime.now()
				conv= f"CRYPTO TO CRYPTO -{amount}{base} TO {quote} =====> IS {new_rate} {quote}"
				conn = sqlite3.connect("database.db")
				cur = conn.cursor()
				cur.execute("INSERT INTO conv('name','conerter','time') VALUES('{}','{}','{}')".format(name,conv,now))
				conn.commit()
				conn.close()
				print("crypto to crypto conversion data inserted into dtabase")

				return render_template("crypto_nex.html",show = msg )
			except:
				msg = "ERROR!"
				return render_template("crypto_nex.html",show = msg)		

# ========================================================================================================== ok 

# history sessions handling 
@app.route("/history",methods =["POST","GET"])
def history():
	if request.method == "GET":
		name = session["user"]
		conn = sqlite3.connect("database.db")
		cur = conn.cursor()
		cur.execute("SELECT conerter,time FROM conv WHERE name ='{}'".format(name))
		data = cur.fetchall()
		print(data)
		# data is a list
		if name == session["user"]:
			return render_template("history.html",data_list = data)
		else:
			return "404"
	else:
		return "ERROR!"
				




# main driver function
if __name__ == '__main__':
	app.run(debug=True)




	