import React, { useState } from 'react'

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    
    function handleSubmit(e) {
        e.preventDefault();
        fetch("/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username }),
        }).then((r) => {
          if (r.ok) {
            r.json().then((user) => onLogin(user));
          }
        });
      }

    return (
        <form onSubmit={handleSubmit}>
            <input 
            type='text' 
            id='username'
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            placeholder='username'
            />
            
            <button type='submit'>Login</button>
        </form>
    );
}


export default Login;
