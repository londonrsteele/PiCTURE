import React, { useState, useEffect } from "react";
import "./Quote.css"

export default function Quote() {
    const [quote, setQuote] = useState({
        quote: "",
        author: ""
    });

    useEffect(() => {
        fetch("/quote").then(res =>
            res.json().then(data => {
                setQuote({
                    quote: data[0].q,
                    author: data[0].a
                });
            })
        );
        const interval = setInterval(() => {
            fetch("/quote").then(res =>
                res.json().then(data => {
                    setQuote({
                        quote: data[0].q,
                        author: data[0].a
                    });
                })
            );
        }, (60 * 60 * 1000)); // every 1 hour (60min*60sec*1000ms)
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="QuoteBox" >
            <div className="Quote">
                {quote.quote}
            </div>
            <div className="Author">
                {quote.author}
            </div>
        </div>
    );
}