from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/api/calcTax", methods=["GET", "POST"])
def calcTax():
  """
  Expects JSON like: {"a": <number>, "b": <number>, "c": <number>}
  Returns: {"tax": <number>}
  """
  if request.method == "POST":
  
    data = request.get_json(silent=True)

    if not data or "a" not in data or "b" not in data or "c" not in data:
      return jsonify({"error1": "Income can not be blank"}), 400
    

    try:
      a = float(data["a"])
      b = float(data["b"])
      c = float(data["c"])

      session["empl"] = a
      session["savings"] = a
      session["bonus"] = a
      

      if a < 0 or b < 0 or c < 0:
        return jsonify({"error2": "Please provide positive income"}), 400
      savings_tax = 0
      if b > 1000:
        savings_tax = 15/100*(b-1000)
      if a < 25000:
        bonus_tax = 20/100*c
      elif 25000 < a < 50000:
        bonus_tax = 40/100*c
      else:
        bonus_tax = 45/100*c
        
      return jsonify({"taxIncome": 20/100*a, "taxSavings": savings_tax, "taxBonus": bonus_tax}), 200
      
    except (ValueError, TypeError):
      return jsonify({"error4": "All incomes must be numerical"}), 400
    
    return render_template("index.html")

  
@app.route("/api/saveTax", methods=["POST"])
def commit_sum():
  data = request.get_json(silent=True)
  
  try:
    a = float(data["a"])
    b = float(data["b"])
    
    # this is where we save the inputs in a db
    #import db_manager
    #db_manager.addIncomes(1, a, b)

    return jsonify({"message": "Saved"}), 200
    
  except (ValueError, TypeError):
    return jsonify({"error": "Error saving"}), 400


if __name__ == "__main__":
    app.run(debug=True)
