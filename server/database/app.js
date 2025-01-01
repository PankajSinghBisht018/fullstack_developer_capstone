const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.log(error);
  res.status(500).json({ error: 'Error fetching documents' });
}


// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealerships.find({}); // Fetch all dealerships
    res.status(200).json(dealers);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error fetching dealerships');
  }
});

// Express route to fetch dealerships by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const dealers = await Dealerships.find({ state: state }); // Query by state
    res.status(200).json(dealers);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error fetching dealerships by state');
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id); // Convert the id to a number
    const dealer = await Dealerships.findOne({ id: id }); // Use the 'id' field
    if (!dealer) {
      return res.status(404).send('Dealer not found');
    }
    res.status(200).json(dealer);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error fetching dealer by ID');
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = documents[0]['id'] + 1;

  const review = new Reviews({
    "id": new_id,
    "name": data['name'],
    "dealership": data['dealership'],
    "review": data['review'],
    "purchase": data['purchase'],
    "purchase_date": data['purchase_date'],
    "car_make": data['car_make'],
    "car_model": data['car_model'],
    "car_year": data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
