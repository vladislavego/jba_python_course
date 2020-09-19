from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def ask_user():
    return input("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")


def print_tasks(tasks, task_description_format="day", message_if_empty="Nothing to do!"):
    if tasks:
        task_position = 1
        if task_description_format == "day":
            for task in tasks:
                print(f"{task_position}. {task.task}")
                task_position += 1
        elif task_description_format == "all":
            for task in tasks:
                print(f"{task_position}. {task.task}. {task.deadline.strftime('%d')} {task.deadline.strftime('%b')}")
                task_position += 1
    else:
        print(message_if_empty)


def get_day_tasks(day_number=None):
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day_number is None:
        tasks = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        print()
        print(f"Today {datetime.today().strftime('%d')} {datetime.today().strftime('%b')}:")
    else:
        tasks = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(day_number)).all()
        current_day = datetime.today() + timedelta(day_number)
        day_name = week_days[current_day.weekday()]
        print()
        print(f"{day_name} {current_day.strftime('%d')} {current_day.strftime('%b')}:")
    print_tasks(tasks)


def get_week_tasks():
    days_in_week = 7
    for day in range(days_in_week):
        get_day_tasks(day)


def get_all_tasks():
    print()
    print("All tasks:")
    tasks = session.query(Table).order_by(Table.deadline).all()
    print_tasks(tasks, "all")


def get_missed_tasks():
    print()
    print("Missed tasks:")
    tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print_tasks(tasks, "all", "There's no missed tasks")


def delete_task():
    print()
    print("Choose the number of the task you want to delete:")
    tasks = session.query(Table).order_by(Table.deadline).all()
    print_tasks(tasks, "all", "Nothing to delete")
    if tasks:
        delete = int(input())
        row_to_delete = tasks[delete - 1]
        session.delete(row_to_delete)
        session.commit()
        print("The task has been deleted!")


def add_new_task():
    print()
    task_description = input("Enter task\n")
    deadline = input("Enter deadline\n")
    new_task = Table(task=task_description, deadline=datetime.strptime(deadline, f"%Y-%m-%d"))
    session.add(new_task)
    session.commit()
    print("The task has been added!")


def start_to_do_list():
    what_to_do = ask_user()

    while what_to_do != "0":

        if what_to_do == '1':
            get_day_tasks()
        elif what_to_do == '2':
            get_week_tasks()
        elif what_to_do == '3':
            get_all_tasks()
        elif what_to_do == '4':
            get_missed_tasks()
        elif what_to_do == '5':
            add_new_task()
        elif what_to_do == '6':
            delete_task()
        else:
            print("Wrong command")
        what_to_do = ask_user()

    print()
    print("Bye!")


start_to_do_list()

