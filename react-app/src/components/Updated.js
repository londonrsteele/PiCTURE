import React, { useState, useEffect } from "react";
export default function Updated() {
    const [time, setTime] = useState({
        time: ""
    });

    useEffect(() => {
        fetch("/updated").then(res =>
            res.json().then(data => {
                setTime({
                    time: data.time
                });
            })
        );
    }, []);

    return (
        <div className="Updated" >
            Last updated: {time.time}
        </div>
    );
}