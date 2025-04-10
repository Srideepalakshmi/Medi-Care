const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json()); // To parse JSON request bodies

// MongoDB Connection
mongoose.connect('mongodb+srv://medi-care:srideepa@17@medicare-cluster.ib986vh.mongodb.net/', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.error("❌ MongoDB connection error:", err));

// Contact Schema and Model
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    message: { type: String, required: true },
});

const Contact = mongoose.model("Contact", contactSchema);

// Contact Form API Route
app.post("/contact", async (req, res) => {
    try {
        const { name, email, phone, message } = req.body;

        // Validation
        if (!name || !email || !phone || !message) {
            return res.status(400).json({ message: "All fields are required!" });
        }

        const newContact = new Contact({ name, email, phone, message });
        await newContact.save();
        res.status(201).json({ message: "Query submitted successfully!" });
    } catch (error) {
        console.error("Error saving contact:", error);
        res.status(500).json({ message: "Error saving data", error });
    }
});

// Start Server on port 5002
const PORT = 5002;
app.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
});
