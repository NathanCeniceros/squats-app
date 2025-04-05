import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './App.css';

function App() {
  const [date, setDate] = useState(new Date());
  const [progress, setProgress] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);

  useEffect(() => {
    fetch(`https://your-backend-url.com/api/progress/${date.toISOString().split('T')[0]}`)
      .then((response) => response.json())
      .then((data) => setProgress(data));
  }, [date]);

  const toggleSlot = (index) => {
    fetch(`/api/progress/${date.toISOString().split('T')[0]}/${index}`, {
      method: 'POST',
    })
      .then((response) => response.json())
      .then(() => {
        const updatedProgress = [...progress];
        updatedProgress[index] = !updatedProgress[index];
        setProgress(updatedProgress);
      });
  };

  return (
    <div className="App">
      <h1>Squats Tracker</h1>
      <Calendar onChange={setDate} value={date} />
      <h2>Progress for {date.toDateString()}</h2>
      <div className="time-slots">
        {progress.map((completed, index) => (
          <button
            key={index}
            className={completed ? 'completed' : 'pending'}
            onClick={() => toggleSlot(index)}
          >
            {timeSlots[index]} {completed ? '✔' : '✗'}
          </button>
        ))}
      </div>
    </div>
  );
}

export default App;
