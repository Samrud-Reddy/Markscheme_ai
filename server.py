from flask import Flask, render_template, jsonify, request
import utility

app = Flask(__name__, template_folder="website/templates", static_folder="website/static")



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search_paper():
    code = request.args.get('code')
    question = request.args.get('question')

    results = utility.search_db(code, question)
    

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

