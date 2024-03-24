import icalendar
import datetime
import sqlite3

def get_weekly_tasks():
    with open('weekly_tasks.ics', encoding='UTF-8') as f:
        cal = icalendar.Calendar.from_ical(f.read())
    event_list = []
    try:
        for event in cal.walk('vevent'):
            if event.get('dtstart').dt.strftime('%Y-%m-%d') >= datetime.datetime.now().strftime('%Y-%m-%d') and event.get('dtstart').dt.strftime('%Y-%m-%d') <= (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'):
                events = {
                    'date' : event.get('dtstart').dt.strftime('%Y-%m-%d'),
                    'summary' : event.get('summary'),
                    'time' : event.get('dtstart').dt.strftime('%H:%M')
                }
                event_list.append(events)
    except Exception as e:
        print(e)

    return event_list

def store_weekly_tasks():
    conn = sqlite3.connect('db/weekly_tasks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS weekly_tasks (date TEXT, summary TEXT, time TEXT)')
    conn.commit()
    conn.close()

    for event in get_weekly_tasks():
        conn = sqlite3.connect('db/weekly_tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO weekly_tasks (date, summary, time) VALUES (?, ?, ?)', (event['date'], event['summary'], event['time']))
        conn.commit()
        conn.close()

store_weekly_tasks()