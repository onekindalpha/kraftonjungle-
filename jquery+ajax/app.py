from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("ajax.html")

@app.route("/cat")
def cat():
    return render_template("cat.html")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5004, debug=True)