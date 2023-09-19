from flask import jsonify, request
import json
from uuid import uuid4


def database_read():
    try:
        with open("database.json", "r") as openfile:

            return json.load(openfile)

    except:

        return []


def database_write(records):
    with open("database.json", "w") as outfile:
        json.dump(records, outfile)


def user_add():
    post_data = request.form if request.form else request.json

    user = {
        "user_id": str(uuid4()),
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone_number": "",
        "active": True,
    }

    for field in ["first_name", "last_name", "email", "phone_number"]:
        try:
            user[field] = post_data[field]
        except:
            pass

    user_records = database_read()

    user_records.append(user)

    database_write(user_records)

    return jsonify(f"added user: {user}"), 201


def users_get_all():
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records found"), 404

    return jsonify(user_records), 200


def user_get_by_id(user_id):
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records found"), 404

    for user in user_records:
        if user["user_id"] == user_id:
            return jsonify(f"user found: {user}"), 200

    return jsonify("no user record found"), 404


def user_update(user_id):
    post_data = request.form if request.form else request.json

    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records found"), 404

    for user in user_records:
        if user["user_id"] == user_id:
            for key in user.keys():
                try:
                    user[key] = post_data[key]
                except:
                    pass

            database_write(user_records)
            return jsonify(f"updated user: {user}"), 200

    return jsonify("no user record found"), 404


def user_activity(user_id):
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records found"), 404

    for user in user_records:
        if user["user_id"] == user_id:
            user["active"] = not user["active"]
            database_write(user_records)

            if user["active"]:
                return jsonify("user has been activated"), 200
            else:
                return jsonify("user has been deactivated"), 200

    return jsonify("no user record found"), 404


def user_delete(user_id):
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records found"), 404

    for index, user in enumerate(user_records):
        if user["user_id"] == user_id:
            del user_records[index]
            database_write(user_records)
            return jsonify("user has been removed"), 200

    return jsonify("no user record found"), 404
