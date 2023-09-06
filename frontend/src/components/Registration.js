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

