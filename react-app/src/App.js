import './App.css';
import DateTime from "./components/Time";
import WiFi from "./components/WiFi";
import Updated from "./components/Updated";
import Calendar from "./components/Calendar";
import Quote from "./components/Quote";
import Weather from "./components/Weather"

function App() {
    return (
        <div className="App">
            <div className="Weather">
                <Weather />
            </div>
            <div className="BottomRow">
                <div className="LeftColumn">
                    <div className="Calendar">
                        <Calendar />
                    </div>
                </div>
                <div className="RightColumn">
                    <div className="QOTD">
                        <Quote />
                    </div>
                    <div className="Clock">
                        <DateTime />
                    </div>
                    <div className="Status">
                        <Updated />
                        <WiFi />
                    </div>
                </div>
            </div>
        </div>
  );
}

export default App;
