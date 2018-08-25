from flask import Flask, jsonify
import AutoLike

app = Flask(__name__)

@app.route('/AutoLike', methods=['GET'])
def AutoLikeRequest():
    print "Auto like controller started"
    autoLikePost = AutoLike.AutoLike()
    autoLikePost.MainAutoLiker()
    return "Auto like controller finished", 200

if __name__ == '__main__':
    app.run(debug=True)