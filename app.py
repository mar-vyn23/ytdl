from flask import Flask, render_template


# Specify the templates folder explicitly
app = Flask(__name__, template_folder="templates")

# Define the route correctly
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    print(app.url_map)
