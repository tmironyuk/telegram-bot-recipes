from utils.db_api.sqlite import Database


def test():
    db = Database()

    db.create_table_users()
    users = db.select_all_users()
    print(f"Пользователи: {users}")
    db.add_user(10, "One", "time1", 'username')
    db.add_user(2, "Vasya", "time2")
    db.add_user(8, "John", "john@mail.com")

    users = db.select_all_users()
    print(f"Пользователи: {users}")

    db.create_table_reviews()
    db.add_review(2, "name", "time1", 'review1', 'un')
    db.add_review(4, "name", "time1", 'review2', 'un')
    db.add_review(7, "name", "time1", 'review3', 'un')

    review = db.select_all_reviews()
    print(f"Отзывы: {review}")



    db.create_table_statistics()
    statistics = db.get_statistics()
    statistics = db.set_table_statistics()
    print(f"Статистика: {statistics}")
    db.add_fail()
    db.add_fail()
    db.add_victory()
    db.add_victory()
    db.add_fail()

    statistics = db.get_statistics()
    print(f"Статистика: {statistics}")



test()