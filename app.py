from flask import Flask, render_template, jsonify, request
import os
from backend import get_stats
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update_stats():
    player1_name = request.args.get('player1Name')
    player1_tag = request.args.get('player1Tag')
    player2_name = request.args.get('player2Name')
    player2_tag = request.args.get('player2Tag')
    server = request.args.get('server')
    set_number = request.args.get('setNumber')

    if not all([player1_name, player1_tag, player2_name, player2_tag,
                server, set_number]):
        return jsonify({'error': 'Missing player information'})

    try:
        stats = get_stats(player1_name, player1_tag, player2_name, player2_tag,
                          server, int(set_number))
        if 'error' not in stats:
            stats['set_number'] = int(set_number)
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error updating stats: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
