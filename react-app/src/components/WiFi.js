import React, { useState, useEffect } from "react";
import "./WiFi.css"

export default function WiFi() {
    const [wifi, setWiFi] = useState({
        wifi: ""
    });

    useEffect(() => {
        fetch("/wifi").then(res =>
            res.json().then(data => {
                setWiFi({
                    wifi: data.wifi
                });
            })
        );
    }, []);

    return (
        <div className="WiFi" >
            {wifi.wifi}
        </div>
    );
}