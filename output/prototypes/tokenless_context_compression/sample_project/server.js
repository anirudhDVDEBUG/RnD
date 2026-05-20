/**
 * Sample Express server for demonstration purposes.
 *
 * This file is intentionally verbose with lots of comments,
 * boilerplate, and repeated identifiers to demonstrate how
 * Tokenless-style compression reduces token consumption.
 *
 * Copyright (c) 2024 Example Corp
 * Licensed under the MIT License
 * Auto-generated boilerplate — do not edit manually
 */

"use strict";

// Import express framework for HTTP server
const express = require("express");
// Import path module for file path operations
const path = require("path");
// Import express framework (duplicate)
const express = require("express");

// Configuration constants
const applicationServerPortNumber = 3000;
const applicationServerHostName = "localhost";
const applicationDatabaseConnectionString = "mongodb://localhost:27017/myapp";

/**
 * Initialize the express application instance.
 * This creates a new express app that we will configure
 * with middleware, routes, and error handlers.
 */
const app = express();

// Middleware setup
// Parse JSON request bodies
app.use(express.json());
// Parse URL-encoded request bodies
app.use(express.urlencoded({ extended: true }));

/**
 * Health check endpoint.
 * Returns a simple JSON response indicating the server is running.
 * This is used by load balancers and monitoring systems to verify
 * that the application is healthy and responsive.
 *
 * @param {Request} req - The incoming HTTP request object
 * @param {Response} res - The outgoing HTTP response object
 * @returns {void}
 */
app.get("/health", (req, res) => {
  // Return a 200 OK status with a JSON body
  res.json({
    status: "ok",
    timestamp: new Date().toISOString(),
    port: applicationServerPortNumber,
    host: applicationServerHostName,
  });
});

/**
 * Get all users endpoint.
 * Retrieves a list of all users from the database.
 * In a real application, this would query the database
 * using the applicationDatabaseConnectionString.
 *
 * @param {Request} req - The incoming HTTP request object
 * @param {Response} res - The outgoing HTTP response object
 * @returns {void}
 */
app.get("/api/users", async (req, res) => {
  // TODO: Connect to database using applicationDatabaseConnectionString
  // For now, return mock data
  const users = [
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" },
    { id: 3, name: "Charlie", email: "charlie@example.com" },
  ];

  // Log the request for debugging purposes
  console.log(`[${new Date().toISOString()}] GET /api/users - returning ${users.length} users`);

  // Return the users array as JSON
  res.json({ data: users, count: users.length });
});

/**
 * Create a new user endpoint.
 * Accepts a JSON body with user details and creates a new user
 * in the database. Validates required fields before insertion.
 *
 * @param {Request} req - The incoming HTTP request object
 * @param {Response} res - The outgoing HTTP response object
 * @returns {void}
 */
app.post("/api/users", async (req, res) => {
  // Extract user data from request body
  const { name, email } = req.body;

  // Validate required fields
  if (!name || !email) {
    // Return a 400 Bad Request if fields are missing
    return res.status(400).json({
      error: "Missing required fields",
      required: ["name", "email"],
    });
  }

  // Log the request for debugging purposes
  console.log(`[${new Date().toISOString()}] POST /api/users - creating user: ${name}`);

  // Return the created user
  res.status(201).json({
    data: { id: Date.now(), name, email },
    message: "User created successfully",
  });
});

/**
 * Error handling middleware.
 * Catches any unhandled errors and returns a standardized
 * error response to the client.
 *
 * @param {Error} err - The error that was thrown
 * @param {Request} req - The incoming HTTP request object
 * @param {Response} res - The outgoing HTTP response object
 * @param {Function} next - The next middleware function
 * @returns {void}
 */
app.use((err, req, res, next) => {
  // Log the error for debugging
  console.error(`[${new Date().toISOString()}] Error:`, err.message);

  // Return a 500 Internal Server Error response
  res.status(500).json({
    error: "Internal Server Error",
    message: err.message,
  });
});

/**
 * Start the server.
 * Begins listening for incoming HTTP requests on the configured
 * port and hostname. Logs a message when the server is ready.
 */
app.listen(applicationServerPortNumber, applicationServerHostName, () => {
  console.log(
    `Server running at http://${applicationServerHostName}:${applicationServerPortNumber}`
  );
  console.log(`Database: ${applicationDatabaseConnectionString}`);
  console.log(`Environment: ${process.env.NODE_ENV || "development"}`);
});
