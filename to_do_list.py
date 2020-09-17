# Write your code here
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
4) Add task
0) Exit
""")


def get_day_tasks(day_number=None):
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day_number is None:
        tasks = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        print()
        print(f"Today {datetime.today().strftime('%d')} {datetime.today().strftime('%b')}:")
    else:
        tasks = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(day_number)).all()
        current_day = datetime.today() + timedelta(day)
        day_name = week_days[current_day.weekday()]
        print()
        print(f"{day_name} {current_day.strftime('%d')} {current_day.strftime('%b')}:")
    if tasks:
        task_position = 1
        for task in tasks:
            print(f"{task_position}. {task.task}")
            task_position += 1
    else:
        print("Nothing to do!")


def get_all_tasks():
    all_tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    task_position = 1
    for task in all_tasks:
        print(f"{task_position}. {task.task}. {task.deadline.strftime('%d')} {task.deadline.strftime('%b')}")
        task_position += 1


def add_new_task():
    task_description = input("Enter task\n")
    deadline = input("Enter deadline\n")
    new_task = Table(task=task_description, deadline=datetime.strptime(deadline, f"%Y-%m-%d"))
    session.add(new_task)
    session.commit()
    print("The task has been added!")


what_to_do = ask_user()

while what_to_do != "0":

    if what_to_do == "1":
        get_day_tasks()
    elif what_to_do == "2":
        for day in range(7):
            get_day_tasks(day)
    elif what_to_do == "3":
        get_all_tasks()
    elif what_to_do == "4":
        print()
        add_new_task()
    else:
        print("Wrong command")
    what_to_do = ask_user()

print()
print("Bye!")

