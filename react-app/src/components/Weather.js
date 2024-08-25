import React, { useState, useEffect } from "react";
import "./Weather.css"

export default function Weather() {
    const [weather, setWeather] = useState({
        latitude: "",
        longitude: "",
        temperature: ""
    });

    useEffect(() => {
        fetch("/weather").then(res =>
            res.json().then(data => {
                setWeather({
                    latitude: data.latitude,
                    longitude: data.longitude,
                    temperature: data.current[0].temperature
                });
            })
        );
    }, []);

    return (
        <div className="Weather" >
            {weather.latitude}, {weather.longitude}
            Current Temperature: {weather.temperature}
        </div>
    );
}