from flask import Flask, jsonify, request
from roguelike.engine import Game

app = Flask(__name__)

# Global game instance
game = Game()

@app.route('/', methods=['GET'])
def get_game_state():
    return jsonify(game.to_dict())

@app.route('/action', methods=['POST'])
def perform_action():
    data = request.get_json()
    action = data.get('action')
    if action:
        game.step(action)
    return jsonify(game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
