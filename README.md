# Daygraise

A minimal task manager and graphing tool to visualize productivity

## Description

If there is an origin of happiness for a high school student,
it is crossing out to-do list. To make my life more interesting,
I decided to "appraise" each day based on productivity. For about
a year, I used to list my works in google docs named "그냥 해" and
write a number next to each date. If I think the day was productive,
I increased the number in green from previous productive day. If
not, I increased the number in red from previous unproductive day.
Lastly, I would go to Canva to either increase or decrease the
final number (green - red) to graph my productivity.

The method of managing my tasks worked well for about a year or so
until I started to see lags when opening the document and Canva.
Therefore, I explored different amazing options out there including
Taskwarrior and Todo.txt, in which I definitely enjoyed. However,
I didn't want to lose that sensation when you cross out a task and
graph your productivity from my previous method. Therefore, I decided
to build one myself where Daygraise is a composite word of "day" and
"appraise".

Daygraise is a minimal viable product that has the ability to manage
your daily task, tasks with due dates, and most importantly evaluate
the productivity visually. This project is entirely written in Python
to integrate json files readily. The tasks will be managed with three
json files: `archive.json`, `today.json`, and `later.json`. Daily
tasks will be stored in `today.json` and tasks with due dates that
does not have to be completed that day are stored in `later.json`.
Lastly, `archive.json` will be used to log the previous days and
visualize the productivity. Furthermore, Daygraise utilize
[Matplotlib](https://matplotlib.org/) to visualize the daily graphs.


## Getting Started
### Installing

* As a minimal viable product that I created for personal use,
I have not created different methods to distribute the program yet.
* To run the program, you can do the following.
1. Clone the repository.
```
git clone
```

2. Enable virtual environment and install dependencies
```
python3 -m venv .venv
pip install -r requirements.txt
```

3. Use [PyInstaller](https://pyinstaller.org/en/stable/)
to make the program executable
```
pyinstaller -F daygraise.py
```

4. Make the executable globally accessible (This may vary depending
on your Operating System)
```
sudo mv dist/daygraise /usr/local/bin/daygraise
```

### Executing Program

* Here are different commands and what to expect :)
* Help
```
daygraise -h
```
* Add or delete task
```
daygraise add/delete today/later "your task" -optional
```
* List the tasks
```
daygraise list
daygriase list today/later
```
* Graph
```
daygraise graph
```

The data will be stored in `~/.local/share/daygraise/data/`
folder.


## Help

Any comments and feedback are welcomed! Please do not
hesitate to create a pull request or contact me
[here](https://enochyu.com/contact/) :)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License.

