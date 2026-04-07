from app import db
from app.utils import logger
from sqlalchemy import desc, exc, or_
import datetime
import traceback


class ChangeRequest(db.Model):
    __tablename__ = "change_request"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, comment="变更控制号")
    created_at = db.Column(db.Date, default=datetime.date.today, comment="发起日期")
    title = db.Column(db.String(200), comment="变更标题")
    description = db.Column(db.String(2000), comment="变更描述")
    department = db.Column(db.String(100), comment="发起部门")
    creator = db.Column(db.String(100), comment="发起人")

    level = db.Column(db.String(50), comment="变更级别")
    impact_assessment = db.Column(db.String(2000), comment="变更影响评估")
    approval_date = db.Column(db.Date, comment="变更批准日期")

    close_date = db.Column(db.Date, comment="变更关闭日期")
    cmo_agreed = db.Column(db.Boolean, comment="CMO是否同意")
    cio_code = db.Column(db.String(50), comment="对应的CIO编号")

    status = db.Column(db.String(20), default="Open", comment="状态: Open/Closed")

    action_items = db.relationship(
        "ActionItem", backref="change_request", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "created_at": str(self.created_at) if self.created_at else None,
            "title": self.title,
            "description": self.description,
            "department": self.department,
            "creator": self.creator,
            "level": self.level,
            "impact_assessment": self.impact_assessment,
            "approval_date": str(self.approval_date) if self.approval_date else None,
            "close_date": str(self.close_date) if self.close_date else None,
            "cmo_agreed": self.cmo_agreed,
            "cio_code": self.cio_code,
            "status": self.status,
        }

    @staticmethod
    def get_list(filter_status=None, filter_action_status=None, keyword=None):
        try:
            query = ChangeRequest.query

            if keyword:
                search = f"%{keyword}%"
                query = query.filter(
                    or_(ChangeRequest.code.like(search), ChangeRequest.title.like(search))
                )

            if filter_status and filter_status != "All":
                if filter_status == "Open":
                    query = query.filter(
                        or_(ChangeRequest.status == "Open", ChangeRequest.status.is_(None))
                    )
                else:
                    query = query.filter(ChangeRequest.status == filter_status)

            if filter_action_status == "Unfinished":
                query = query.filter(
                    ChangeRequest.action_items.any(ActionItem.status != "Done")
                )

            query = query.order_by(ChangeRequest.code.desc())
            requests = query.all()

            result = []
            for req in requests:
                req_dict = req.to_dict()
                if filter_action_status == "Unfinished":
                    actions = req.action_items.filter(ActionItem.status != "Done").all()
                else:
                    actions = req.action_items.all()
                req_dict["action_items"] = [a.to_dict() for a in actions]
                result.append(req_dict)

            return True, result
        except exc.SQLAlchemyError as e:
            logger.error(traceback.format_exc())
            return False, str(e)


class ActionItem(db.Model):
    __tablename__ = "change_action_item"

    id = db.Column(db.Integer, primary_key=True)
    change_id = db.Column(db.Integer, db.ForeignKey("change_request.id"), nullable=False)
    content = db.Column(db.String(1000), comment="行动计划内容")
    owner = db.Column(db.String(100), comment="责任人")
    plan_date = db.Column(db.Date, comment="计划完成时间")
    qa_contact = db.Column(db.String(100), comment="跟进人")
    completed_at = db.Column(db.Date, comment="实际完成时间")
    status = db.Column(db.String(20), default="Pending", comment="状态: Pending/Done")

    def to_dict(self):
        return {
            "id": self.id,
            "change_id": self.change_id,
            "content": self.content,
            "owner": self.owner,
            "plan_date": str(self.plan_date) if self.plan_date else None,
            "qa_contact": self.qa_contact,
            "completed_at": str(self.completed_at) if self.completed_at else None,
            "status": self.status,
        }

    @staticmethod
    def get_list(filter_status=None):
        try:
            query = ActionItem.query.options(db.joinedload(ActionItem.change_request))

            if filter_status == "Unfinished":
                query = query.filter(ActionItem.status != "Done")

            query = query.order_by(ActionItem.plan_date.asc())
            items = query.all()

            result = []
            for item in items:
                data = item.to_dict()
                if item.change_request:
                    data["change_info"] = {
                        "id": item.change_request.id,
                        "code": item.change_request.code,
                        "title": item.change_request.title,
                        "description": item.change_request.description,
                        "department": item.change_request.department,
                        "level": item.change_request.level,
                        "impact_assessment": item.change_request.impact_assessment,
                        "approval_date": str(item.change_request.approval_date) if item.change_request.approval_date else None,
                        "close_date": str(item.change_request.close_date) if item.change_request.close_date else None,
                        "cmo_agreed": item.change_request.cmo_agreed,
                        "cio_code": item.change_request.cio_code,
                        "status": item.change_request.status,
                    }
                result.append(data)

            return True, result
        except exc.SQLAlchemyError as e:
            logger.error(traceback.format_exc())
            return False, str(e)
