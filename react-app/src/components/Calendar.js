import React, { useState, useEffect } from "react";
import "./Calendar.css"

function CalendarItem({ date, name, start, end }) {
    return (
        <div className="CalendarItem">
            <div className="CalendarItem-date">
                {date}
            </div>
            <div className="CalendarItem-name">
                {name}
            </div>
            <div className="CalendarItem-Time">
                <div className="CalendarItem-start">
                    {start}
                </div>
                <div className="CalendarItem-to">
                    to
                </div>
                <div className="CalendarItem-end">
                    {end}
                </div>
            </div>
        </div>
    )
}

export default function Updated() {
    const [calendar, setCalendar] = useState({
        list_of_events: ""
    });

    useEffect(() => {
        fetch("/calendar").then(res =>
            res.json().then(data => {
                setCalendar({
                    list_of_events: data.items
                });
            })
        );
    }, []);

    if (calendar.list_of_events.length === 0) {
        return (
            <div className="CalendarBox" >
                <div className="NoEvents-Sticky">
                    No events!
                </div>
            </div>
        )
    }
    else if (calendar.list_of_events.length === 1) {
        return (
            <div className="CalendarBox" >
                <CalendarItem
                    date={calendar.list_of_events[0].date}
                    name={calendar.list_of_events[0].summary}
                    start={calendar.list_of_events[0].start}
                    end={calendar.list_of_events[0].end}
                />
            </div>
        )
    }
    else if (calendar.list_of_events.length === 2) {
        return (
            <div className="CalendarBox" >
                <CalendarItem
                    date={calendar.list_of_events[0].date}
                    name={calendar.list_of_events[0].summary}
                    start={calendar.list_of_events[0].start}
                    end={calendar.list_of_events[0].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[1].date}
                    name={calendar.list_of_events[1].summary}
                    start={calendar.list_of_events[1].start}
                    end={calendar.list_of_events[1].end}
                />
            </div>
        )
    }
    else if (calendar.list_of_events.length === 3) {
        return (
            <div className="CalendarBox" >
                <CalendarItem
                    date={calendar.list_of_events[0].date}
                    name={calendar.list_of_events[0].summary}
                    start={calendar.list_of_events[0].start}
                    end={calendar.list_of_events[0].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[1].date}
                    name={calendar.list_of_events[1].summary}
                    start={calendar.list_of_events[1].start}
                    end={calendar.list_of_events[1].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[2].date}
                    name={calendar.list_of_events[2].summary}
                    start={calendar.list_of_events[2].start}
                    end={calendar.list_of_events[2].end}
                />
            </div>
        )
    }
    else if (calendar.list_of_events.length === 4) {
        return (
            <div className="CalendarBox" >
                <CalendarItem
                    date={calendar.list_of_events[0].date}
                    name={calendar.list_of_events[0].summary}
                    start={calendar.list_of_events[0].start}
                    end={calendar.list_of_events[0].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[1].date}
                    name={calendar.list_of_events[1].summary}
                    start={calendar.list_of_events[1].start}
                    end={calendar.list_of_events[1].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[2].date}
                    name={calendar.list_of_events[2].summary}
                    start={calendar.list_of_events[2].start}
                    end={calendar.list_of_events[2].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[3].date}
                    name={calendar.list_of_events[3].summary}
                    start={calendar.list_of_events[3].start}
                    end={calendar.list_of_events[3].end}
                />
            </div>
        )
    }
    else if (calendar.list_of_events.length === 5) {
        return (
            <div className="CalendarBox" >
                <CalendarItem
                    date={calendar.list_of_events[0].date}
                    name={calendar.list_of_events[0].summary}
                    start={calendar.list_of_events[0].start}
                    end={calendar.list_of_events[0].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[1].date}
                    name={calendar.list_of_events[1].summary}
                    start={calendar.list_of_events[1].start}
                    end={calendar.list_of_events[1].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[2].date}
                    name={calendar.list_of_events[2].summary}
                    start={calendar.list_of_events[2].start}
                    end={calendar.list_of_events[2].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[3].date}
                    name={calendar.list_of_events[3].summary}
                    start={calendar.list_of_events[3].start}
                    end={calendar.list_of_events[3].end}
                />
                <CalendarItem
                    date={calendar.list_of_events[4].date}
                    name={calendar.list_of_events[4].summary}
                    start={calendar.list_of_events[4].start}
                    end={calendar.list_of_events[4].end}
                />
            </div>
        )
    }
}