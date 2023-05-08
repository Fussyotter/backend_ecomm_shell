# Ecommerce Backend Shell

A Django backend for a small business ecommerce site. This shell contains customizable product models with a variety of specifics to help categorize and search. User Authentication and Stripe Payment are within the shell as well. 

## Installation

1. Clone the repository
2. Navigate into the project directory
3. Set up a virtual environment and install Python dependencies: `pip install -r requirements.txt`
4. Set up environment variables for Stripe API keys and other configuration options: `cp .env.example .env` and update `.env` file with your values.
5. Set up a database: `python3 manage.py migrate`
6. Start development server: `python3 manage.py runserver`

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

## Technologies Used

- Django
- Next.js
- Stripe

## Known Issues

- Payment processing may not work in certain countries or with certain types of cards.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following third-party libraries:

- Django Rest Framework (https://www.django-rest-framework.org/)
- Stripe (https://stripe.com/)
