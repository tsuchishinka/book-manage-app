from auth_service.model.user import User
from auth_service.service.database import Database


def insert_user(user: User):
    # TODO: ユーザーのレコード追加
    user_id = 20
    return user_id


def update_user(database: Database, user: User):
    with database.transaction():
        conn.execute(
            f"""
            UPDATE `user` 
                SET `name` = {user.name}, `mail_address` = {user.mail_address}, `password` = {user.password_hashed}, `role_id` = {user.role_id}
                WHERE `user_id` = {user.user_id}
            """
        )

    return user


def find_user_by_id(user_id: int):
    # TODO: ユーザーIDでユーザーを取得
    return User


def find_user_by_mail_address(mail_address: str):
    # TODO: メールアドレスでユーザーを取得
    return User
