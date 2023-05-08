from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        if name=="magdy" and password=="1234":

            return render_template("secret.html")
        else:
            return "not magdy "
    return "d"




if __name__ == '__main__':
    app.run(debug=True)

