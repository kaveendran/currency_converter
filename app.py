
from flask import Flask,render_template,request,flash
import sqlite3
import requests
API= "NCBIFMP7K04TYN59"
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def start():
	if request.method == "POST":
		# extract data from http post request
		c_from = request.form.get("from")
		c_to = request.form.get("to")
		c_amount = request.form.get("amount")

		print(c_amount)

		
		# c_amount = int(c_amount)
		# test = c_from + c_to + c_amount
		try:
			c_amount_int = int(c_amount)
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

			url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=AAS4L22ZFSLATUZ6'.format(c_from,c_to)
			r = requests.get(url)
			data = r.json()

			print(data)

			# amount * 5. Exchange Rate = amount
			E_rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
			print(E_rate)
			E_rate_c = float(E_rate)
			C_amount = E_rate_c * c_amount_int
			print("Amount{}".format(C_amount))





		
			print_text = "Converted Amount Is {} {}".format(C_amount,c_to)

			return render_template("converter.html",show=print_text)
	else:
		return render_template("converter.html")


# main driver function
if __name__ == '__main__':


	app.run(debug=True)
