const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// ✅ MongoDB Connection
mongoose.connect('mongodb+srv://medi-care:srideepa%4017@medicare-cluster.ib986vh.mongodb.net/reviewDB')
  .then(() => console.log("✅ MongoDB Connected"))
  .catch(err => console.error("❌ MongoDB connection error:", err));

// ✅ Contact Schema & Model
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    message: { type: String, required: true },
}, { timestamps: true });

const Contact = mongoose.model("Contact", contactSchema);

// ✅ Review Schema & Model
const reviewSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    rating: { type: Number, required: true },
    comment: { type: String, required: true },
}, { timestamps: true });

const Review = mongoose.model("Review", reviewSchema);

// ✅ POST: Contact Form Submission
app.post("/api/contact", async (req, res) => {
    try {
        const { name, email, phone, message } = req.body;
        if (!name || !email || !phone || !message) {
            return res.status(400).json({ message: "All contact fields are required." });
        }
        const newContact = new Contact({ name, email, phone, message });
        await newContact.save();
        res.status(201).json({ message: "✅ Contact query submitted successfully." });
    } catch (error) {
        console.error("❌ Error saving contact:", error);
        res.status(500).json({ message: "Error saving contact data." });
    }
});

// ✅ POST: Submit Review
app.post('/api/reviews', async (req, res) => {
    try {
        const { name, email, rating, comment } = req.body;
        if (!name || !email || !rating || !comment) {
            return res.status(400).json({ message: "All review fields are required." });
        }
        const newReview = new Review({ name, email, rating, comment });
        await newReview.save();
        res.status(201).json({ message: "✅ Review submitted successfully." });
    } catch (error) {
        console.error("❌ Error saving review:", error);
        res.status(500).json({ message: "Error saving review." });
    }
});

// ✅ GET: Fetch All Reviews
app.get('/api/reviews', async (req, res) => {
    try {
        const reviews = await Review.find().sort({ createdAt: -1 });
        res.json(reviews);
    } catch (error) {
        console.error("❌ Error fetching reviews:", error);
        res.status(500).json({ message: "Error retrieving reviews." });
    }
});

// ✅ Start Server
const PORT = 5001;
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
