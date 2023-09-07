// import React, { useState } from 'react';
// import { Link } from 'react-router-dom';
// import axios from 'axios';


// axios.defaults.xsrfCookieName = 'csrftoken';
// axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;

// const client = axios.create({
//   baseURL: "http://127.0.0.1:8000"
// });

// function Registration() {
//   const [currentUser, setCurrentUser] = useState();
//   const [email, setEmail] = useState('');
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');

//   const handleRegistration = async (e) => {
//     e.preventDefault();

//     try {
//         // Send a POST request to register
//         const registrationResponse = await client.post("/api/register/", {
//           email: email,
//           username: username,
//           password: password
//         });
    
//         // Check if registration was successful before attempting to log in
//         if (registrationResponse.status === 201) {
//           // Send a POST request to log in
//           const loginResponse = await client.post("/api/login/", {
//             email: email,
//             password: password
//           });
    
//           // Check if login was successful before setting the current user
//           if (loginResponse.status === 200) {
//             setCurrentUser(true);
//           }
//         }
//       } catch (error) {
//         // Handle any errors that occur during registration or login
//         if (error.response) {
//           // If the error has a response from the server, it's likely a validation error
//           const errorData = error.response.data;
          
//           console.log(`validation error: ${error.response.data}`)
//           if (errorData.error === 'Email already exists') {
//             setError('Email already exists');
//           } else if (errorData.error === 'Username already exists') {
//             setError('Username already exists');
//           } else if (errorData.error === 'Password must have at least 8 characters and special characters.') {
//             setError('Password must have at least 8 characters and special characters.');
//           } else {
//             setError('An error occurred during registration.');
//           }
//         } else {
//           // If there's no response (e.g., network error), display a generic error message
//           setError('An error occurred during registration.');
//         }
//       }
//     }

//   return (
//     <div>
//     {currentUser ? (
//       <div>
//         <h2>Welcome, User!</h2>
//         <p>You are already logged in.</p>
//       </div>
//     ) : (
//     <div>
//       <h2>Registration</h2>
//       <form onSubmit={handleRegistration}>
//         <input
//           type="email"
//           placeholder="Email"
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//           required
//         />
//         <input
//           type="text"
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//           required
//         />
//         <input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           required
//         />
//         <button type="submit">Register</button>
//       </form>
//       <p className="error">{error}</p>
//       <p>
//         Already have an account? <Link to="/login">Login here</Link>
//       </p>
//     </div>
//               )}
//               </div>
//   );
// }

// export default Registration;

import * as React from 'react';
import { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Not So Boring Blog
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');


// axios.defaults.xsrfCookieName = 'csrftoken';
// axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;



  const handleRegistration = async (event) => {
    event.preventDefault();
    const registrationData = {
      username: username,
      email: email,
      password: password,
    };

    try {
      const registrationResponse = await axios.post("http://127.0.0.1:8000/api/register/", registrationData);
      if (registrationResponse.status === 201) {
        const loginData = {
          email: registrationData.email,
          password: registrationData.password
        };
        const loginResponse = await axios.post("http://127.0.0.1:8000/api/login/", loginData);
        if (loginResponse.status === 200) {
          console.log('OK 200')
        }
      }
    } catch (error) {
        if (error.response) {
          // If the error has a response from the server, it's likely a validation error
          const errorData = error.response.data;
          
          console.log(`validation error: ${error.response.data}`)
          if (errorData.error === 'Email already exists') {
            setError('Email already exists');
          } else if (errorData.error === 'Username already exists') {
            setError('Username already exists');
          } else if (errorData.error === 'Password must have at least 8 characters and special characters.') {
            setError('Password must have at least 8 characters and special characters.');
          } else {
            setError('An error occurred during registration.');
          }
        } else {
          // If there's no response (e.g., network error), display a generic error message
          setError('An error occurred during registration.');
        }
      }
    }

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box component="form" noValidate onSubmit={handleRegistration} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  autoComplete="username"
                  name="username"
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  autoFocus
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign Up
            </Button>
            <p className="error">{error}</p>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
                  Already have an account? Log in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}
