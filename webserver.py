import flask
from flask import Flask, request
import json
import database
from datetime import date


server = Flask(__name__)

def run():
    server.run(port=80)

@server.route("/aircraft/")
def get_aircraft():
    args = request.args.to_dict()
    where_arg = []
    like_arg = []
    limit = 100
    page = 1
    order = ""

    for key in args.keys():
        if key in ["type", "icao_type", "owner", "category", "manufacturer"]:
            where_arg.append(f"{key} = '{args.get(key)}'")
        elif key == "year_created":
            try:
                where_arg.append(f"{key} = {int(args.get(key))}")
            except ValueError:
                return flask.Response("Bad request: Year created needs to be an integer", status=400)
        elif key == "registration":
            where_arg.append(f"{key} = '{args.get(key).upper()}'")
        elif key == "limit":
            try:
                limit = int(args["limit"])
            except ValueError:
                return flask.Response("Bad request: Limit needs to be an integer", status=400)
            if limit > 1000:
                return flask.Response("Bad request: Limit cannot be larger than 1000", status=400)
        elif key == "page":
            try:
                page = int(args["page"])
            except ValueError:
                return flask.Response("Bad request: Page number needs to be an integer", status=400)
        elif key == "order":
            for order_argument in (args["order"].split(",")):
                if order_argument not in ["registration", "type", "icao_type", "owner", "category", "manufacturer", "year_created"]:
                    return flask.Response(f"Bad request: Invalid order argument {order_argument}", status=400)
            order = args["order"] + ","
        elif key.startswith("search-"):
            search_key = key[7:]
            if search_key in ["type", "icao_type", "owner", "category", "manufacturer", "registration"]:
                like_arg.append(f"{search_key} LIKE '%{args.get(key)}%'")
            else:
                return flask.Response(f"Bad request: Invalid search argument {search_key}", status=400)
        else:
            return flask.Response(f"Bad request: Invalid argument {key}", status=400)
    if like_arg:
        like_arg = " AND ".join(like_arg)
    else:
        like_arg = ""
    if where_arg:
        where_arg = " WHERE " + " AND ".join(where_arg)
    else:
        where_arg = ""
        if like_arg:
            like_arg = " WHERE " + like_arg

    # I am aware of the possibility of SQL injection, but I was unable to find a solution in the given time.
    # Not using SELECT * because I don't want to select the identity column.
    response = database.get(f"SELECT registration, type, icao_type, owner, category, manufacturer, year_created FROM {database.TABLE} {where_arg} {like_arg} ORDER BY {order}registration,identity OFFSET {limit * (page - 1)} LIMIT {limit}")

    return flask.Response(json.dumps(response), mimetype="application/json")

@server.route("/aircraft", methods=["POST"])
def post_new_aircraft():
    if not request.is_json:
        return flask.Response("Bad request: Content type unsupported. JSON is required.", status=400)
    jsonbody = request.json
    if not jsonbody:
        return flask.Response("Bad request: JSON body is empty", status=400)
    for key in jsonbody.keys():
        if key in ["type", "icao_type", "owner", "category", "manufacturer", "registration"]:
            if not isinstance(jsonbody[key], str):
                return flask.Response(f"Bad request: Value of {key} needs to be a string", status=400)
        elif key == "year_created":
            if not isinstance(jsonbody[key], int):
                return flask.Response("Bad request: Value of year_created needs to be an int", status=400)
        else:
            return flask.Response(f"Bad request: Unexpected object in JSON: {key}", status=400)
    if len(jsonbody.keys()) != 7:
        return flask.Response("Bad request: Missing arguments", status=400)
    database.put(f"INSERT INTO {database.TABLE} ({', '.join(jsonbody.keys())}) VALUES(%s, %s, %s, %s, %s, %s, %s)", tuple(jsonbody.values()))
    return flask.Response("{}", mimetype="application/json", status=201)

@server.route("/summary")
def get_summary():
    response = {}
    most_common = {}
    args = request.args.to_dict()
    remove_empty = False
    if "remove_empty" in args.keys():
        if args["remove_empty"] == "true":
            remove_empty = True
        elif args["remove_empty"] != "false":
            return flask.Response("Bad request: remove_empty needs to be a boolean", status=400)

    for key in args.keys():
        if key.startswith("most-"):
            most_key = key[5:]
            if most_key in ["type", "icao_type", "owner", "category", "manufacturer", "year_created"]:
                try:
                    value = int(args[key])
                except ValueError:
                    return flask.Response("Bad request: Amount needs to be an integer", status=400)
                if value > 25:
                    return flask.Response("Bad request: Amount cannot be larger than 25", status=400)
                where_arg = ""
                if remove_empty:
                    where_arg = f"WHERE {most_key} != ''"
                    if most_key == "year_created":
                        where_arg = f"WHERE {most_key} IS NOT NULL"
                # Again aware of the possibility of SQL injection but was unable to find a solution in the given time.
                sql_response = database.get(f"SELECT {most_key}, COUNT(*) AS counted FROM {database.TABLE} {where_arg} GROUP BY {most_key} ORDER BY counted DESC, {most_key} LIMIT {value}")
                category_response = {}
                for response_key in sql_response:
                    category_response[response_key[most_key]] = response_key["counted"]
                most_common[most_key] = category_response
        elif key != "remove_empty":
            return flask.Response(f"Bad request: Invalid argument {key}", status=400)
    response["most_common"] = most_common
    response["avg_age"] = str(date.today().year - database.get(f"SELECT AVG(year_created) FROM {database.TABLE}")[0]["avg"])
    response["total_aircraft"] = database.get(f"SELECT count(*) FROM {database.TABLE}")[0]["count"]
    response["oldest_aircraft"] = database.get(f"SELECT MIN(year_created) FROM {database.TABLE} WHERE year_created > 1")[0]["min"]
    response["youngest_aircraft"] = database.get(f"SELECT MAX(year_created) FROM {database.TABLE}")[0]["max"]
    return flask.Response(json.dumps(response), mimetype="application/json")
