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