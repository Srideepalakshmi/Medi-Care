const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json()); // Parse JSON request bodies

// MongoDB Connection
mongoose.connect('mongodb+srv://medi-care:srideepa%4017@medicare-cluster.ib986vh.mongodb.net/reviewDB', {
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

// Review Schema and Model
const reviewSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    rating: { type: Number, required: true },
    comment: { type: String, required: true },
});
const Review = mongoose.model("Review", reviewSchema);

// Contact Form API
app.post("/contact", async (req, res) => {
    try {
        const { name, email, phone, message } = req.body;
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

// Review Form API - POST
app.post("/api/reviews", async (req, res) => {
    try {
        const { name, email, rating, comment } = req.body;
        if (!name || !email || !rating || !comment) {
            return res.status(400).json({ message: "All review fields are required!" });
        }

        const newReview = new Review({ name, email, rating, comment });
        await newReview.save();
        res.status(201).json({ message: "Review submitted successfully!" });
    } catch (error) {
        console.error("Error saving review:", error);
        res.status(500).json({ message: "Error saving review", error });
    }
});

// Review List API - GET
app.get("/api/reviews", async (req, res) => {
    try {
        const allReviews = await Review.find();
        res.json(allReviews);
    } catch (error) {
        console.error("Error fetching reviews:", error);
        res.status(500).json({ message: "Error retrieving reviews", error });
    }
});

// Start Server
const PORT = 5002;
app.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
});
