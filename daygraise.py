# DAYGRAISE

# Imports
import json
import os
import argparse
from pathlib import Path
import datetime


# File Paths
TODAY = Path("~/.local/share/daygraise/data/today.json").expanduser()
LATER = Path("~/.local/share/daygraise/data/later.json").expanduser()
ARCHIVE = Path("~/.local/share/daygraise/data/archive.json").expanduser()


# Argparse
parser = argparse.ArgumentParser(
                    prog='Daygraise',
                    usage='Daygraise action location value [--optional] [-h]',
                    description='A task manager and a productivity visualizer',
                    epilog=None)
parser.add_argument(
            'action',
            help='add, delete, list, graph, rate')
parser.add_argument(
            'location',
            nargs='?',
            help='today, later')
parser.add_argument(
            'value',
            nargs='?',
            help='tasks, good/bad')
parser.add_argument('-o', '--optional', help='Add urgency or deadline')

args = parser.parse_args()


# ------------------------------------------------
# Basic FUNCTIONS
# ------------------------------------------------
# Making files for the first time
def make_json():
    date = datetime.date.today().isoformat()

    # Archive
    if not ARCHIVE.exists():
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        with open(ARCHIVE, "w") as f:
            json.dump(
                [
                    {
                      "date": date,
                      "score": 0,
                      "tasks": []
                    }
                ],
                f, indent=2
            )

    # Today
    if not TODAY.exists():
        TODAY.parent.mkdir(parents=True, exist_ok=True)
        with open(TODAY, "w") as f:
            json.dump(
                {
                  "date": date,
                  "score": 0,
                  "tasks": []
                },
                f, indent=2
            )

    # Later
    if not LATER.exists():
        LATER.parent.mkdir(parents=True, exist_ok=True)
        with open(LATER, "w") as f:
            json.dump({"tasks": []}, f, indent=2)


# Reusable Functions
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# ------------------------------------------------
# Tasks FUNCTIONS
# ------------------------------------------------
# Adding Tasks
def add_today(name, urgency):
    data = load_data(TODAY)
    data["tasks"].append({
        "name": name,
        "urgency": urgency,
        "completed": False
    })

    save_data(TODAY, data)
    print(f"Successfully added '{name}'")

def add_later(name, deadline):
    data = load_data(LATER)
    data["tasks"].append({
        "name": name,
        "deadline": deadline,
        "completed": False
    })

    save_data(LATER, data)
    print(f"Successfully added '{name}'")


# Deleting Tasks
def delete_today(name):
    data = load_data(TODAY)

    for task in data["tasks"]:
        if task["name"] == name:
            task["completed"] = True

            save_data(TODAY, data)
            print(f"Successfully deleted '{name}'")

            break
    else:
        print(f"The task '{name}' does not exist")

def delete_later(name):
    data = load_data(LATER)

    for task in data["tasks"]:
        if task["name"] == name:
            data["tasks"].remove(task)

            save_data(LATER, data)
            print(f"Successfully deleted '{name}'")

            break
    else:
        print(f"The task '{name}' does not exist")


# List Tasks
def list_today():
    data = load_data(TODAY)
    list_task = False
    counter = 1

    print("     Tasks for today               Urgency        ")
    print("--------------------------------------------------")

    for task in data["tasks"]:
        if not task["completed"]:
            name = task["name"]
            urgency = task["urgency"]

            print(f" {counter}. {name:<20} {urgency if urgency else '':<3}")
            list_task = True
            counter += 1
    print()

    if not list_task:
        print("You have no tasks for today!")

def list_later():
    data = load_data(LATER)
    list_task = False
    counter = 1

    print("     Tasks for later                 Deadline     ")
    print("--------------------------------------------------")

    for task in data["tasks"]:
        name = task["name"]
        deadline = task["deadline"]

        print(f" {counter}. {name:<20} {deadline if deadline else '':<10}")

        list_task = True
        counter += 1
    print()

    if not list_task:
        print("You have no tasks for later!")

def list_tasks():
    today_data = load_data(TODAY)
    later_data = load_data(LATER)
    today_tasks = today_data["tasks"]
    later_tasks = later_data["tasks"]
    list_task = False

    today_counter = 1
    later_counter = 1

    row_num = max(len(today_tasks), len(later_tasks))

    print("     Tasks for Today           Tasks for Later    ")
    print("--------------------------------------------------")

    for i in range(row_num):
        if i < len(today_tasks):
            today_task = today_tasks[i]
            today_str = f"{today_counter}. {today_task['name']}"
            today_counter += 1
        else:
            today_str = ""

        if i < len(later_tasks):
            later_task = later_tasks[i]
            later_str = f"{later_counter}. {later_task['name']}"
            later_counter += 1
        else:
            later_str = ""

        print(f" {today_str:<20} | {later_str:<20}")

    list_task = True
    print()

    if not list_task:
        print("You do not have any tasks yet!")


# ------------------------------------------------
# End of the day FUNCTIONS
# ------------------------------------------------
def rate(result):
    data = load_data(TODAY)
    data_archive = load_data(ARCHIVE)
    last_score = data_archive[-1]["score"]

    if result == "good":
        last_score += 1
        data["score"] = last_score
    elif result == "bad":
        last_score += -1
        data["score"] = last_score

    save_data(TODAY, data)
    print("Successfully scored today")


def move_to_archive():
    today_data = load_data(TODAY)
    archive_data = load_data(ARCHIVE)

    archive_data.append(today_data)
    save_data(ARCHIVE, archive_data)

    TODAY.unlink(missing_ok=True)

def graph():
    # Faster startup
    import matplotlib.pyplot as plt

    data = load_data(ARCHIVE)
    total = len(data)
    dates = []
    scores = []

    for i in range(total):
        score = data[i]["score"]
        scores.append(score)

    for i in range(total):
        date = data[i]["date"]
        dates.append(date)


    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Daygraise")

    plt.plot(dates, scores)
    plt.xticks([dates[0], dates[-1]])

    plt.show()


# ------------------------------------------------
# Finale
# ------------------------------------------------
# Dashboard
def dashboard():
    os.system("cls" if os.name == "nt" else "clear")
    print("==================================================")
    print("Welcome Back!")
    print(f"Last login: {datetime.datetime.now():%H:%M %Y-%m-%d}")
    print("==================================================\n")
    parser.print_help()
    print()


# Execute
def main():
    make_json()
    dashboard()

    if args.action == "list":
        if args.location == "today":
            list_today()
        elif args.location == "later":
            list_later()
        else:
            list_tasks()

    elif args.action == "graph":
        graph()

    elif args.action == "rate":
        rate(args.location)
        move_to_archive()
        make_json()

    elif args.action == "add":
        if args.location == "today":
            add_today(args.value, args.optional)
        elif args.location == "later":
            add_later(args.value, args.optional)

    elif args.action == "delete":
        if args.location == "today":
            delete_today(args.value)
        elif args.location == "later":
            delete_later(args.value)


if __name__ == '__main__':
    main()


