import React, { useState, useEffect } from "react";
import "./Updated.css"

export default function Updated() {
    const [time, setTime] = useState({
        time: ""
    });

    useEffect(() => {
        const interval = setInterval(() => {
            fetch("/updated").then(res =>
                res.json().then(data => {
                    setTime({
                        time: data.time
                    });
                })
            );
        }, (60*1000)); // every 1 min (60sec*1000ms)
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="Updated" >
            Last updated: {time.time}
        </div>
    );
}