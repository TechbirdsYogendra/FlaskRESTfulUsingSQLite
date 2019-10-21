from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Please pass price as well"
                        )

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return {"item": {"name": item[0], "price": item[1]}}
        return {"message": "Item not found"}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        print(result)
        item = result.fetchone()

        connection.close()
        return item

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    def post(self, name):
        item = Item.find_by_name(name)
        if item:
            return {"message": f"The item with name {name} is already exist."}, 400
        request_data = Item.parser.parse_args()

        item = {"name": name, "price": request_data["price"]}
        try:
            Item.insert_item(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500  # Internal Server Error
        return item, 201

    def delete(self, name):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {"message": "Item Deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                Item.insert_item(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                Item.update_item(updated_item)
            except:
                return {"message": "An error occurred updating the item"}, 500

        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        all_items = []
        rows = cursor.execute(query)
        for row in rows:
            item = {"name": row[0], "price": row[1]}
            all_items.append(item)

        connection.close()
        return {"items": all_items}
