from flask import Flask, request, jsonify, send_file
import psycopg2
from config import config

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')
@app.route('/api/products', methods=['GET'])
def get_products():
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        #get query parameters from the request
        columns = request.args.get('columns')
        criteria = request.args.get('criteria')
        query = f"SELECT {columns} FROM inventory"
        if criteria:
            query += f" WHERE {criteria}"

        # Execute the SQL query
        crsr.execute(query)
        # Fetch all rows
        products = crsr.fetchall()
        crsr.close()
        connection.close()
        #convert the fetched data to JSON format and return as response
        return jsonify(products)
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}),500
    except Exception as e:
        return jsonify({'error': str(e)}),500
if __name__ == "__main__":
    app.run(debug=True)