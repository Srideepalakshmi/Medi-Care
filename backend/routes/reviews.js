const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const Review = require('backend/models/Review.js'); // adjust path if needed

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect('mongodb+srv://medi-care:srideepa%4017@medicare-cluster.ib986vh.mongodb.net/reviewDB', {
    // you can omit useNewUrlParser and useUnifiedTopology for Mongoose 7+
}).then(() => console.log("MongoDB connected"));

app.post('/api/reviews', async (req, res) => {
    const { name, email, rating, comment } = req.body;
    const newReview = new Review({ name, email, rating, comment });
    await newReview.save();
    res.json({ message: "Review saved" });
});

app.get('/api/reviews', async (req, res) => {
    const reviews = await Review.find().sort({ createdAt: -1 });
    res.json(reviews);
});
const PORT = 5001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

