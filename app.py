@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    collection.insert_one(todo_item)

    return jsonify({
        "message": "To-Do item submitted successfully"
    })