# Ecommerce Backend Shell

A Django backend for a small business ecommerce site. This shell contains customizable product models with a variety of specifics to help categorize and search. User Authentication and Stripe Payment are within the shell as well. The frontend is built with Next.js and can be found here: `https://github.com/Fussyotter/ecommShell`.   The intention for this shell is a base for small ecommerce sites that can be customized to fit the needs of the business.  For more specific uses of Stripe Payment, please see the Stripe documentation.  This shell is not intended to be a full ecommerce site, but a starting point for a small business to build upon.  Currently Checkout for cart is fully functional but for your specific use adjust webhooks as needed.

## Installation

1. Clone the repository
2. Navigate into the project directory
3. Set up a virtual environment and install Python dependencies: `pip install -r requirements.txt`
4. Set up environment variables for Stripe API keys and other configuration options: `cp .env.example .env` and update `.env` file with your values.
5. Set up a database: `python3 manage.py migrate`
6. Start development server: `python3 manage.py runserver`
<!-- Optional for testing -->
7. run loaddata to load the initial data: `python3 loadData.py`
8. run imageLoadTest.py to load the images: `python3 imageLoadTest.py`

## Environment Variables

The following environment variables are required to run the application:

SECRET_KEY: Django secret key
DEBUG: Set to True for development, False for production
ALLOWED_HOSTS: Comma-separated list of allowed hosts for the application
DATABASE_URL: Connection URL for the database (e.g. postgres://username:password@hostname/database)
STRIPE_SECRET_KEY: Stripe secret key
STRIPE_PUBLIC_KEY: Stripe public key

## Usage

1. Browse products by category or search for specific items.
2. Add items to your shopping cart and view the contents of your cart.
3. Proceed to checkout and enter your payment information.
4. View your order history and track the status of your orders.

## Features

- Search functionality to find products by name, category, or price range.
- User authentication and authorization.
- Secure payment processing using Stripe.
- Order history and status tracking for logged-in users.
- low level implementation of GPT-2 for SQL queries.

## Technologies Used

- Django
- Stripe
- Pytorch
- Transformers
  

## Known Issues

- Payment processing may not work in certain countries or with certain types of cards.
- GPT-2 responses can be broad, requests need to be specific to db structure

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following third-party libraries:

- Django Rest Framework (https://www.django-rest-framework.org/)
- Stripe (https://stripe.com/)
