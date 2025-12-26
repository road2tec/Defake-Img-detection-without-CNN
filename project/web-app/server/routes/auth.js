const router = require('express').Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// Register
router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Validation
        if (!username || !password) {
            return res.status(400).json({ msg: 'Please enter all fields' });
        }
        if (password.length < 6) {
            return res.status(400).json({ msg: 'Password must be at least 6 characters' });
        }

        // Check for existing user
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ msg: 'User already exists' });
        }

        // Hash password
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const newUser = new User({
            username,
            password: hashedPassword
        });

        const savedUser = await newUser.save();

        res.json({
            user: {
                id: savedUser._id,
                username: savedUser.username
            }
        });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Login
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Validation
        if (!username || !password) {
            return res.status(400).json({ msg: 'Please enter all fields' });
        }

        // Check for user
        const user = await User.findOne({ username });
        if (!user) {
            return res.status(400).json({ msg: 'User does not exist' });
        }

        // Validate password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ msg: 'Invalid credentials' });
        }

        // Sign Token
        const token = jwt.sign(
            { id: user._id },
            process.env.JWT_SECRET || 'secret_key_change_me',
            { expiresIn: 3600 } // 1 hour
        );

        res.json({
            token,
            user: {
                id: user._id,
                username: user.username
            }
        });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
