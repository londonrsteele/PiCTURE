import React, { useState, useEffect } from "react";
import "./Time.css";

export default function DateTime() {
    const [datetime, setDateTime] = useState({
        dow: "",
        month: "",
        date: "",
        year: "",
        time: "",
        ampm: ""
    });

    useEffect(() => {
        fetch("/time").then(res =>
            res.json().then(data => {
                setDateTime({
                    dow: data.dow,
                    month: data.month,
                    date: data.date,
                    year: data.year,
                    time: data.time,
                    ampm: data.ampm
                });
            })
        );
    }, []);

    return (
        <div className="DateTimeBox">
            <div className="TimeBox">
                <div className="Time">
                    {datetime.time}
                </div>
                <div className="AMPM">
                    {datetime.ampm}
                </div>
            </div>
            <div className="DateBox">
                <div className="DOW">
                    {datetime.dow}
                </div>
                <div className="Month">
                    {datetime.month}
                </div>
                <div className="Date">
                    {datetime.date}
                </div>
            </div>
        </div>
    );
}