from flask import Flask, jsonify
import AutoLike

app = Flask(__name__)

@app.route('/AutoLike', methods=['GET'])
def AutoLikeController():
    AutoLike.MainAutoLiker()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)