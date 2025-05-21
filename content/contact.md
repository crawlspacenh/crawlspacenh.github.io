+++
title = 'Contact & Booking'
date = 2025-05-20T12:00:00-04:00
draft = false
+++
<!-- markdownlint-disable MD025 MD033 MD045 -->

<style>
  .contact-container {
    font-family: "Lora", serif;
    font-size: 21px;
    line-height: 33px;
    letter-spacing: -0.2px;
    color: #848d96;
    margin-bottom: 40px;
  }

  .contact-container h1, .contact-container h2 {
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
    color: #47bec7;
    margin-top: 35px;
  }

  .contact-container a {
    color: #848d96;
    transition-duration: 0.5s;
    border-bottom: 1px dotted #848d96;
  }

  .contact-container a:hover {
    color: #CA486d;
    transition-duration: 0.1s;
    border-bottom: 1px dotted #CA486d;
  }

  .contact-form {
    margin-top: 30px;
    max-width: 600px;
  }

  .form-group {
    margin-bottom: 25px;
  }

  .form-group label {
    display: block;
    margin-bottom: 8px;
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
    font-size: 0.9em;
  }

  .form-group input, .form-group textarea, .form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid rgba(132, 141, 150, 0.3);
    background-color: rgba(6, 28, 48, 0.7);
    border-radius: 4px;
    font-family: "Lora", serif;
    font-size: 0.9em;
    color: #848d96;
  }

  .form-group textarea {
    min-height: 150px;
    resize: vertical;
  }

  .submit-button {
    background-color: #47bec7;
    color: #061C30;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
    font-size: 1em;
    transition: background-color 0.3s ease;
  }

  .submit-button:hover {
    background-color: #CA486d;
  }

  .contact-info {
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid rgba(132, 141, 150, 0.2);
  }

  .contact-method {
    margin-bottom: 20px;
  }

  .contact-method i {
    margin-right: 10px;
    color: #47bec7;
  }
</style>

<div class="contact-container">

# Contact & Booking

Are you interested in booking Crawlspace for your venue, private event, or festival? We'd love to hear from you! Fill out the form below or reach out directly using our contact information.

## Booking Inquiry Form

<form class="contact-form" action="https://formspree.io/f/mzzrwwny" method="POST">
  <div class="form-group">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>
  </div>
  <div class="form-group">
    <label for="phone">Phone (optional)</label>
    <input type="tel" id="phone" name="phone">
  </div>
  <div class="form-group">
    <label for="venue">Venue/Event Name</label>
    <input type="text" id="venue" name="venue" required>
  </div>
  <div class="form-group">
    <label for="event-type">Event Type</label>
    <select id="event-type" name="event-type" required>
      <option value="">Select an option</option>
      <option value="bar-club">Bar/Club</option>
      <option value="festival">Festival</option>
      <option value="private">Private Event</option>
      <option value="corporate">Corporate Event</option>
      <option value="other">Other</option>
    </select>
  </div>
  <div class="form-group">
    <label for="date">Preferred Date(s)</label>
    <input type="text" id="date" name="date" required>
  </div>
  <div class="form-group">
    <label for="message">Additional Details</label>
    <textarea id="message" name="message" required></textarea>
  </div>
  <button type="submit" class="submit-button">Send Inquiry</button>
</form>

<div class="contact-info">
  <h2>Direct Contact</h2>
  <div class="contact-method">
    <strong>Email:</strong> booking@crawlspacenh.com
  </div>

  <p>We typically respond to all inquiries within 24-48 hours. For urgent booking matters, please call the number above.</p>

  <h2>Technical Requirements</h2>
  <p>Crawlspace is a five-piece band consisting of three guitars, bass, and drums with multiple vocalists. We can provide our own PA system for smaller venues, but have technical requirements for larger spaces.</p>
  <p>For detailed technical specifications or to request our full technical rider, please email <a href="mailto:tech@crawlspacenh.com">tech@crawlspacenh.com</a>.</p>
</div>

</div>
