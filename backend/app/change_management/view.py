from flask import request, Blueprint, send_file, jsonify
from .controller import ChangeManagementHandler
from app.utils.input_output import json_output
from datetime import datetime

bp = Blueprint("change_management", __name__, url_prefix="/api/change")


@bp.route("/list", methods=["GET"])
@json_output
def list_changes():
    filter_status = request.args.get("status")
    filter_action_status = request.args.get("action_status")
    keyword = request.args.get("keyword")
    handler = ChangeManagementHandler()
    return handler.get_changes(filter_status, filter_action_status, keyword)


@bp.route("/action/list", methods=["GET"])
@json_output
def list_actions():
    filter_status = request.args.get("status")
    handler = ChangeManagementHandler()
    return handler.get_action_items(filter_status)


@bp.route("/create", methods=["POST"])
@json_output
def create_change():
    data = request.json
    if "creator" not in data or not data["creator"]:
        data["creator"] = "Admin"
    handler = ChangeManagementHandler()
    return handler.create_change(data)


@bp.route("/update/<int:change_id>", methods=["POST"])
@json_output
def update_change(change_id):
    data = request.json
    handler = ChangeManagementHandler()
    return handler.update_change(change_id, data)


@bp.route("/delete/<int:change_id>", methods=["POST"])
@json_output
def delete_change(change_id):
    handler = ChangeManagementHandler()
    return handler.delete_change(change_id)


@bp.route("/export", methods=["GET"])
def export_changes_view():
    filter_status = request.args.get("status")
    keyword = request.args.get("keyword")
    handler = ChangeManagementHandler()
    ret, result = handler.export_changes(filter_status, keyword)
    if not ret:
        return jsonify({"success": 0, "data": result})
    filename = f"变更流程导出_{datetime.now().strftime('%Y%m%d%H%M')}.xlsx"
    return send_file(
        result,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@bp.route("/action/add", methods=["POST"])
@json_output
def add_action():
    data = request.json
    change_id = data.get("change_id")
    if not change_id:
        return False, "Missing change_id"
    handler = ChangeManagementHandler()
    return handler.add_action_item(change_id, data)


@bp.route("/action/update/<int:item_id>", methods=["POST"])
@json_output
def update_action(item_id):
    data = request.json
    handler = ChangeManagementHandler()
    return handler.update_action_item(item_id, data)


@bp.route("/action/delete/<int:item_id>", methods=["POST"])
@json_output
def delete_action(item_id):
    handler = ChangeManagementHandler()
    return handler.delete_action_item(item_id)
