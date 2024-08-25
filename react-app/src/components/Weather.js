import React, { useState, useEffect } from "react";
import "./Weather.css"

export default function Weather() {
    const [weather, setWeather] = useState({
        // Lat and Lon
        latitude: "",
        longitude: "",
        // Current data
        temperature: "",
        relative_humidity: "",
        feels_like_temp: "",
        day_or_night: "",
        precipitation: "",
        weather_code: "",
        cloud_cover: "",
        wind_speed: "",
        // Daily data
        max_temp: "",
        min_temp: "",
        sunrise: "",
        sunset: "",
        daylight_duration: ""
    });

    useEffect(() => {
        fetch("/weather").then(res =>
            res.json().then(data => {
                setWeather({
                    // Lat and Lon
                    latitude: data.latitude,
                    longitude: data.longitude,
                    // Current data
                    temperature: data.current[0].temperature,
                    relative_humidity: data.current[0].relative_humidity,
                    feels_like_temp: data.current[0].feels_like_temp,
                    day_or_night: data.current[0].day_or_night,
                    precipitation: data.current[0].precipitation,
                    weather_code: data.current[0].weather_code,
                    cloud_cover: data.current[0].cloud_cover,
                    wind_speed: data.current[0].wind_speed,
                    // Daily data
                    max_temp: data.daily[0].max_temp,
                    min_temp: data.daily[0].min_temp,
                    sunrise: data.daily[0].sunrise,
                    sunset: data.daily[0].sunset,
                    daylight_duration: data.daily[0].daylight_duration
                });
            })
        );
    }, []);

    return (
        <div className="Weather" >
            {weather.latitude}, {weather.longitude}<br />
            Current Temperature: {weather.temperature}<br />
        </div>
    );
}