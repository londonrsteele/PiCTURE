import React, { useState, useEffect } from "react";
import "./Weather.css"

export default function Weather() {
    const [weather, setWeather] = useState({
        latitude: "",
        longitude: ""
    });

    useEffect(() => {
        fetch("/weather").then(res =>
            res.json().then(data => {
                setWeather({
                    latitude = data.latitude,
                    longitude = data.longitude
                });
            })
        );
    }, []);

    return (
        <div className="Weather" >
            {weather.latitude}, {weather.longitude}
        </div>
    );
}