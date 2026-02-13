// Test script to verify API connectivity
const fetch = require('node-fetch');

async function testApiConnection() {
    try {
        console.log('Testing API connection...');

        // Test the signup endpoint
        const response = await fetch('http://localhost:8000/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: 'testuser',
                email: 'test@example.com',
                password: 'testpassword123'
            })
        });

        console.log(`Response status: ${response.status}`);

        if (response.ok) {
            const data = await response.json();
            console.log('Signup successful:', data.user);
        } else {
            const errorData = await response.json();
            console.log('Signup failed:', errorData);
        }
    } catch (error) {
        console.error('Connection error:', error.message);
        console.log('This confirms the "Failed to fetch" error is likely due to network connectivity.');
    }
}

testApiConnection();