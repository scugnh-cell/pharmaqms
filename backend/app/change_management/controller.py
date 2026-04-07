from app import db
from app.utils import logger
from .model import ChangeRequest, ActionItem
from datetime import datetime
import traceback
import io
from openpyxl import Workbook


class ChangeManagementHandler:
    def get_changes(self, filter_status=None, filter_action_status=None, keyword=None):
        return ChangeRequest.get_list(filter_status, filter_action_status, keyword)

    def get_action_items(self, filter_status=None):
        return ActionItem.get_list(filter_status)

    def export_changes(self, filter_status=None, keyword=None):
        ret, changes = ChangeRequest.get_list(filter_status=filter_status, keyword=keyword)
        if not ret:
            return False, changes

        wb = Workbook()
        ws = wb.active
        ws.title = "变更流程"

        headers = [
            "变更控制号", "发起日期", "变更标题", "变更描述",
            "发起部门", "变更级别", "变更影响评估", "变更批准日期",
            "变更行动计划及完成情况", "变更关闭日期", "CMO是否同意", "对应的CMO编号",
        ]
        ws.append(headers)

        for c in changes:
            actions_str = ""
            if c.get("action_items"):
                lines = []
                for idx, act in enumerate(c["action_items"], 1):
                    status_cn = "已完成" if act["status"] == "Done" else "待处理"
                    line = f"{idx}. [{act['owner']}] {act['content']} ({status_cn})"
                    if act.get("plan_date"):
                        line += f" 计划:{act['plan_date']}"
                    if act.get("completed_at"):
                        line += f" 实际:{act['completed_at']}"
                    lines.append(line)
                actions_str = "\n".join(lines)

            row = [
                c.get("code"), c.get("created_at"), c.get("title"), c.get("description"),
                c.get("department"), c.get("level"), c.get("impact_assessment"),
                c.get("approval_date"), actions_str, c.get("close_date"),
                "是" if c.get("cmo_agreed") else "否", c.get("cio_code"),
            ]
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return True, output

    def create_change(self, data):
        try:
            required = ["code", "title", "department", "creator"]
            for f in required:
                if f not in data or not data[f]:
                    return False, f"Missing required field: {f}"

            change = ChangeRequest(
                code=data["code"],
                title=data["title"],
                description=data.get("description"),
                department=data["department"],
                creator=data["creator"],
                level=data.get("level"),
                created_at=datetime.strptime(data["created_at"], "%Y-%m-%d").date()
                if data.get("created_at") else datetime.today().date(),
                status="Open",
            )
            db.session.add(change)
            db.session.commit()
            return True, change.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(traceback.format_exc())
            return False, str(e)

    def update_change(self, change_id, data):
        try:
            change = ChangeRequest.query.get(change_id)
            if not change:
                return False, "Change request not found"

            if "title" in data: change.title = data["title"]
            if "description" in data: change.description = data["description"]
            if "level" in data: change.level = data["level"]
            if "impact_assessment" in data: change.impact_assessment = data["impact_assessment"]

            if "approval_date" in data and data["approval_date"]:
                change.approval_date = datetime.strptime(data["approval_date"], "%Y-%m-%d").date()

            if "close_date" in data and data["close_date"]:
                change.close_date = datetime.strptime(data["close_date"], "%Y-%m-%d").date()

            if "cmo_agreed" in data: change.cmo_agreed = data["cmo_agreed"]
            if "cio_code" in data: change.cio_code = data["cio_code"]

            if "status" in data:
                change.status = data["status"]
                if change.status == "Closed" and not change.close_date:
                    change.close_date = datetime.today().date()
                if change.status == "Open":
                    change.close_date = None

            db.session.commit()
            return True, change.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(traceback.format_exc())
            return False, str(e)

    def add_action_item(self, change_id, data):
        try:
            if not data.get("content") or not data.get("owner"):
                return False, "Content and Owner are required"

            item = ActionItem(
                change_id=change_id,
                content=data["content"],
                owner=data["owner"],
                qa_contact=data.get("qa_contact"),
                plan_date=datetime.strptime(data["plan_date"], "%Y-%m-%d").date()
                if data.get("plan_date") else None,
                status="Pending",
            )
            db.session.add(item)
            db.session.commit()
            return True, item.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(traceback.format_exc())
            return False, str(e)

    def update_action_item(self, item_id, data):
        try:
            item = ActionItem.query.get(item_id)
            if not item:
                return False, "Action item not found"

            if "content" in data: item.content = data["content"]
            if "owner" in data: item.owner = data["owner"]
            if "plan_date" in data and data["plan_date"]:
                item.plan_date = datetime.strptime(data["plan_date"], "%Y-%m-%d").date()
            if "qa_contact" in data: item.qa_contact = data["qa_contact"]

            if "status" in data:
                item.status = data["status"]
                if "completed_at" in data and data["completed_at"]:
                    item.completed_at = datetime.strptime(data["completed_at"], "%Y-%m-%d").date()
                elif item.status == "Done" and not item.completed_at:
                    item.completed_at = datetime.today().date()
                if item.status != "Done":
                    item.completed_at = None

            db.session.commit()
            return True, item.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(traceback.format_exc())
            return False, str(e)

    def delete_action_item(self, item_id):
        try:
            item = ActionItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
            return True, "Deleted"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def delete_change(self, change_id):
        try:
            change = ChangeRequest.query.get(change_id)
            if change:
                db.session.delete(change)
                db.session.commit()
            return True, "Deleted"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
