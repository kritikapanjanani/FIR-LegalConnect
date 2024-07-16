// frontend/app.js

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
  
    if (signupForm) {
      signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
  
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        try {
          const response = await fetch('http://localhost:5000/api/auth/signup', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert('Sign up successful!');
            window.location.href = 'login.html';
          } else {
            alert(data.msg || 'Sign up failed');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      });
    }
  
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
  
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        try {
          const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert('Log in successful!');
            // Store the token in localStorage or cookies for authenticated requests
            localStorage.setItem('token', data.token);
            window.location.href = 'index.html';
          } else {
            alert(data.msg || 'Log in failed');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      });
    }
  });
  