const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const FLASK_API_URL = process.env.FLASK_API_URL || "http://backend:5000";

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "form.html"));
});

app.post("/submit", async (req, res) => {
    try {
        await axios.post(
            `${FLASK_API_URL}/submit`,
            new URLSearchParams(req.body).toString(),
            { headers: { "Content-Type": "application/x-www-form-urlencoded" }, timeout: 10000 }
        );

        res.send(`
            <h1>Form Submitted Successfully</h1>
            <p>Student data submitted to Flask backend.</p>
            <a href="/">Go Back</a>
        `);
    } catch (error) {
        console.error("Backend Error:", error.message);

        res.status(500).send(`
            <h1>Error</h1>
            <p>Unable to connect to Flask backend.</p>
            <a href="/">Go Back</a>
        `);
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Frontend running on port ${PORT}`);
});
