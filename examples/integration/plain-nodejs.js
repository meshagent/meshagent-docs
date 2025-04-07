// index.js
const express = require('express');
const bodyParser = require('body-parser');
const { websocketRoomUrl, participantToken } = require('meshagent');

const app = express();

const JWT_SECRET = 'your_jwt_secret';
const URL = 'https://api.meshagent.com';

app.use(bodyParser.json());

// Example of user "database"
const users = [
  {
    id: 1,
    username: 'john',
    password: 'password123'
  },
  {
    id: 2,
    username: 'jane',
    password: 'mypassword'
  },
];

/**
 * POST /authorize-meshagent-user
 *
 * This route simulates user authentication. 
 *
 * On successful validation of username and password,
 * it returns a JWT token for the user.
 */
app.post('/authorize-user', (req, res) => {
  const { username, password } = req.body;

  const url = websocketRoomUrl({roomName});
  const token = participantToken({participantName, roomName, role});

  // Find a matching user in our "database"
  const user = users.find((u) => u.username === username && u.password === password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Generate a JWT token with the user's info
  // In a real-world scenario, you might add roles, permissions, etc.
  const token = jwt.sign(
    {
      userId: user.id,
      username: user.username
    },
    JWT_SECRET,
    { expiresIn: '1h' } // token expires in 1 hour
  );

  return res.json({ 
    url: URL,
    jwt: jwt,
  });
});

// Start the Express server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Client service running on http://localhost:${PORT}`);
});

