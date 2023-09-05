import './App.css';
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function App() {

  const [currentUser, setCurrentUser] = useState();
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    client.get("/api/user/")
    .then(function(res) {
      setCurrentUser(true);
    })
    .catch(function(error) {
      setCurrentUser(false);
    });
  }, []);

  function update_form_btn() {
    if (registrationToggle) {
      document.getElementById("form_btn").innerHTML = "Register";
      setRegistrationToggle(false);
    } else {
      document.getElementById("form_btn").innerHTML = "Log in";
      setRegistrationToggle(true);
    }
  }

  async function submitRegistration(e) {
    e.preventDefault();
  
    try {
      // Send a POST request to register
      const registrationResponse = await client.post("/api/register/", {
        email: email,
        username: username,
        password: password
      });
  
      // Check if registration was successful before attempting to log in
      if (registrationResponse.status === 201) {
        // Send a POST request to log in
        const loginResponse = await client.post("/api/login/", {
          email: email,
          password: password
        });
  
        // Check if login was successful before setting the current user
        if (loginResponse.status === 200) {
          setCurrentUser(true);
        }
      }
    } catch (error) {
      // Handle any errors that occur during registration or login
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

  function submitLogin(e) {
    e.preventDefault();
    client.post(
      "/api/login/",
      {
        email: email,
        password: password
      }
    ).then(function(res) {
      setCurrentUser(true);
    })
    .catch(function(error){
      setError("Invalid email or password");
    });
  }

  function submitLogout(e) {
    e.preventDefault();
    client.post(
      "/api/logout/",
      {withCredentials: true}
    ).then(function(res) {
      setCurrentUser(false);
    });
  }

  if (currentUser) {
    return (
      <div>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand>Authentication App</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                <form onSubmit={e => submitLogout(e)}>
                  <Button type="submit" variant="light">Log out</Button>
                </form>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
          <div className="center">
            <h2>You're logged in!</h2>
          </div>
        </div>
    );
  }
  return (
    <div>
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>Authentication App</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            <Button id="form_btn" onClick={update_form_btn} variant="light">Register</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    {
      registrationToggle ? (
        <div className="center">
          <Form onSubmit={e => submitRegistration(e)} action="/api/register/" method="post">
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicError">
              <Form.Text className="text-danger">
              {error}
              </Form.Text>
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>        
      ) : (
        <div className="center">
          <Form onSubmit={e => submitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicError">
              <Form.Text className="text-danger">
              {error}
              </Form.Text>
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>
      )
    }
    </div>
  );
}

export default App;
