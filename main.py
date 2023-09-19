from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db = mysql.connector.connect(
   host = 'localhost',
   user = 'root',
   password = 'root',
   database = 'api_python'
)

# Rota para criar um novo usuário
@app.route('/users/create', methods = ['POST'])
def create_user():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha, telefone) VALUES (%s, %s, %s, %s)",
                       (nome, email, senha, telefone))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Usuário cadastrado com sucesso'})
    except Exception as error:
        db.rollback()
        cursor.close()
        return jsonify({'error': str(error)})

# Rota para obter todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        cursor.close()

        usuarios_list = []
        for user in users:
            usuario = {
                'id': user[0],
                'nome': user[1],
                'email': user[2],
                'senha': user[3],
                'telefone': user[4]
            }
            usuarios_list.append(usuario)

        return jsonify(usuarios_list)
    except Exception as error:
        cursor.close()
        return jsonify({'error': str(error)})

# Rota para atualizar um usuário
@app.route('/users/<int:user_id>', methods = ['PATCH'])
def update_user(user_id):
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')

    cursor = db.cursor()
    try:
        cursor.execute("UPDATE usuarios SET nome = %s, email = %s, senha = %s, telefone = %s WHERE id = %s",
                       (nome, email, senha, telefone, user_id))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Usuário atualizado com sucesso'})
    except Exception as error:
        db.rollback()
        cursor.close()
        return jsonify({'error': str(error)})

# Rota para excluir um usuário
@app.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Usuário excluído com sucesso'})
    except Exception as error:
        db.rollback()
        cursor.close()
        return jsonify({'error': str(error)})

if __name__ == '__main__':
   app.run(debug=True)
