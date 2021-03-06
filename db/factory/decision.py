from db import connect
from db.model import Basic, Decision
from sqlalchemy import and_


class DecisionFactory:
    @staticmethod
    def get_by_user(user_id):
        """
        Get by user id

        :param int user_id: user id
        :return: decisions
        :rtype: list[Decision]
        """
        session = connect()

        columns = [
            Decision,
            Basic.title_id,
            Basic.title_type,
            Basic.description,
            Basic.image_url
        ]

        query = session \
            .query(*columns) \
            .join(Basic, Decision.title_id == Basic.title_id) \
            .filter(Decision.user_id == user_id)

        try:
            return query.all()
        finally:
            session.close()

    @staticmethod
    def save(decision):
        """
        Save decision

        :param Decision decision: decision object
        """
        session = connect()

        try:
            session.add(decision)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def remove(user_id, title_id):
        """
        Remove decision

        :param int user_id: user id
        :param str title_id: title id
        """
        session = connect()
        filters = [
            Decision.user_id == user_id,
            Decision.title_id == title_id
        ]

        try:
            session.query(Decision).filter(and_(*filters)).delete()
            session.commit()
        finally:
            session.close()
