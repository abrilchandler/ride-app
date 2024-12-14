import React, { useState } from 'react'

function Register({onRegister}) {
    const [username, setUsername] = useState('')
    const [message, setMessage] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json' },
            body: JSON.stringify({username}) 
        });
        if (response.ok) {
            const user = await response.json();
            console.log(user)
            onRegister(user);
            setMessage('Registration successful!');
        } else {
            const errorData = await response.json();
            setMessage(`Error: ${errorData.error}`);
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input
            type='text'
            id='username'
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder='Enter username' />
            <button type='submit'>Register</button>
            {message && <p>{message}</p>}
        </form>
    )
}

export default Register;