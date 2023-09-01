from flask import Flask, request, jsonify, url_for
import uuid

app = Flask(__name__)
messages = []

class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.id = str(uuid.uuid4())  # Gera um UUID único

@app.route('/messages', methods=['GET'])
def get_messages():
    response = {
        'messages': [
            {
                'id': msg.id,
                'author': msg.author,
                'content': msg.content,
                'links': [
                    {'rel': 'self', 'href': url_for('get_message', message_id=msg.id, _external=True)},
                ]
            }
            for msg in messages
        ]
    }
    return jsonify(response)

@app.route('/messages/<message_id>', methods=['GET'])
def get_message(message_id):
    message = next((msg for msg in messages if msg.id == message_id), None)
    if message:
        response = {
            'message': {
                'id': message.id,
                'author': message.author,
                'content': message.content,
                'links': [
                    {'rel': 'self', 'href': url_for('get_message', message_id=message.id, _external=True)}
                ]
            }
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    author = data.get('author')
    content = data.get('content')
    if author and content:
        message = Message(author, content)
        messages.append(message)
        return jsonify({'message': 'Message created', 'id': message.id}), 201
    else:
        return jsonify({'error': 'Author and content are required'}), 400

@app.route('/messages/<int:message_id>', methods=['PUT'])
def edit_message(message_id):
    message = next((msg for msg in messages if msg.id == message_id), None)
    if message:
        data = request.get_json()
        message.author = data.get('author', message.author)
        message.content = data.get('content', message.content)
        return jsonify({'message': 'Message updated', 'id': message.id}), 200
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
