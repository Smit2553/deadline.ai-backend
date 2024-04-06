import icalendar
import datetime
import sqlite3
import uuid

def clear_tasks():
    conn = sqlite3.connect('db/tasks.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS weekly_tasks')
    c.execute('DROP TABLE IF EXISTS all_tasks')
    conn.commit()
    conn.close()
    return True

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
                    'time' : event.get('dtstart').dt.strftime('%H:%M'),
                    'description' : event.get('description'),
                    'location' : event.get('location'),
                    'id' : str(uuid.uuid4()),
                    'status' : 0
                }
                event_list.append(events)
    except Exception as e:
        print(e)

    return event_list

def store_weekly_tasks():
    clear_tasks()
    conn = sqlite3.connect('db/tasks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS weekly_tasks (date TEXT, summary TEXT, time TEXT, description TEXT, location TEXT, id TEXT, status INTEGER DEFAULT 0)')
    conn.commit()
    conn.close()

    for event in get_weekly_tasks():
        conn = sqlite3.connect('db/tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO weekly_tasks (date, summary, time, description, location, id, status) VALUES (?, ?, ?, ?, ?, ?, ?)', (event['date'], event['summary'], event['time'], event['description'], event['location'], event['id'], event['status'] ))
        conn.commit()
        conn.close()
    return True

def get_all_tasks():

    with open('weekly_tasks.ics', encoding='UTF-8') as f:
        cal = icalendar.Calendar.from_ical(f.read())
    event_list = []
    try:
        for event in cal.walk('vevent'):
            events = {
                'date' : event.get('dtstart').dt.strftime('%Y-%m-%d'),
                'summary' : event.get('summary'),
                'time' : event.get('dtstart').dt.strftime('%H:%M'),
                'description' : event.get('description'),
                'location' : event.get('location'),
                'id' : str(uuid.uuid4()),
                'status' : 0
                
            }
            event_list.append(events)
    except Exception as e:
        print(e)
    return event_list

def store_all_tasks():
    clear_tasks()
    conn = sqlite3.connect('db/tasks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS all_tasks (date TEXT, summary TEXT, time TEXT, description TEXT, location TEXT, id TEXT, status INTEGER DEFAULT 0)')
    conn.commit()
    conn.close()

    for event in get_all_tasks():
        conn = sqlite3.connect('db/tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO all_tasks (date, summary, time, description, location, id, status) VALUES (?, ?, ?, ?, ?, ?, ?)', (event['date'], event['summary'], event['time'], event['description'], event['location'], event['id'], event['status']))
        conn.commit()
        conn.close()
    return True
