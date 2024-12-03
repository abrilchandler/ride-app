import React, { useState } from 'react'

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const {password, setPassword} = useState('');
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });

        if (response.ok) {
            onLogin();
        } else {
            alert('Login failed');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type='text' value={username} onChange={(e) => setUsername(e.target.value)} placeholder='username' />
            <input type='text' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='password' />
            <button type='submit'>Login</button>
        </form>
    );
}

export default Login;