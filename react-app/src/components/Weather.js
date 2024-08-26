import React, { useState, useEffect } from "react";
import "./Weather.css"

export default function Weather() {
    const [weather, setWeather] = useState({
        // Current data
        temperature: "",
        relative_humidity: "",
        feels_like_temp: "",
        day_or_night: "",
        precipitation: "",
        weather_code_str: "",
        weather_code_icon: "",
        cloud_cover: "",
        wind_speed: "",
        // Daily data
        max_temp: "",
        min_temp: "",
        sunrise: "",
        sunset: "",
        daylight_duration_hrs: "",
        daylight_duration_min: ""
    });

    useEffect(() => {
        fetch("/weather").then(res =>
            res.json().then(data => {
                setWeather({
                    // Current data
                    temperature: data.current[0].temperature,
                    relative_humidity: data.current[1].relative_humidity,
                    feels_like_temp: data.current[2].feels_like_temp,
                    day_or_night: data.current[3].day_or_night,
                    precipitation: data.current[4].precipitation,
                    weather_code_str: data.current[5].weather_code_str,
                    weather_code_icon: data.current[6].weather_code_icon,
                    cloud_cover: data.current[7].cloud_cover,
                    wind_speed: data.current[8].wind_speed,
                    // Daily data
                    max_temp: data.daily[0].max_temp,
                    min_temp: data.daily[1].min_temp,
                    sunrise: data.daily[2].sunrise,
                    sunset: data.daily[3].sunset,
                    daylight_duration_hrs: data.daily[4].daylight_duration_hrs,
                    daylight_duration_min: data.daily[5].daylight_duration_min
                });
            })
        );
    }, []);

    return (
        <div className="WeatherBox" >
            <div className="Weather-Code">
                <img src={weather.weather_code_icon} class="Weather-Code-Icon" alt="Weather Code Icon"></img>
                <div className="Weather-Code-Text">{weather.weather_code_str}</div>
            </div>
            <div className="Temperature">
                <div className="Temperature-Now">
                    {weather.temperature}&deg;F
                </div>
                <div className="Temperature-FeelsLike">
                    <b>Feels Like:</b> {weather.feels_like_temp}&deg;F
                </div>
                <div className="Temperature-HiLo">
                    {weather.min_temp}&deg;F  |  {weather.max_temp}&deg;F
                </div>
            </div>
            <div className="Details">
                <b>Humidity:</b> {weather.relative_humidity}% <br />
                <b>Cloud Cover:</b> {weather.cloud_cover}% <br />
                <b>Precip:</b> {weather.precipitation}" <br />
                <b>Wind Speed:</b> {weather.wind_speed}mph
            </div>
            <div className="Sun">
                <div className="Sun-Up">
                    icon <br />
                    {weather.sunrise}
                </div>
                <div className="Sun-Down">
                    icon <br />
                    {weather.sunset}
                </div>
                <div className="Sun-Duration">
                    Hours of Sunlight: <br />
                    {weather.daylight_duration_hrs}:{weather.daylight_duration_min}
                </div>
            </div>
        </div>
    );
}