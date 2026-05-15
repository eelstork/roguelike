from flask import Flask, jsonify, request
from roguelike.engine import Game

app = Flask(__name__)

# Global game instance
game = Game()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def get_game_state():
    return jsonify(game.to_dict())

@app.route('/action', methods=['POST'])
def perform_action():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    action = data.get('action')
    if action:
        game.step(action)
    return jsonify(game.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
