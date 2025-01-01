from flask import Flask, render_template, jsonify
import subprocess

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Serve the HTML page
    return render_template("home.html")



@app.route("/mark", methods=["POST"])
def mark_attendance():
    try:
        # Run recognition.py as a subprocess
        result = subprocess.run(["python", "recognition.py"], capture_output=True, text=True)
        
        # Check if the script ran successfully
        if result.returncode == 0:
            return jsonify({"message": "Attendance marked successfully."})
        else:
            return jsonify({"message": f"Error in recognition script: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
