# Anime Watchlist Web App
### Video Demo: https://youtu.be/iIducjzrMdc
### Table of Contents

- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech_stack)
- [Technical Details](#technical_details)
- [Database Schema](#database_schema)
- [Future Improvements](#future_improvements)

## Description

The Anime Watchlist Web App is designed to elevate your anime viewing experience by providing a comprehensive platform for managing and discovering anime. This web application allows users to efficiently search for anime, manage their watchlist, and explore new titles. Whether you’re looking to organize your current watchlist or find new recommendations, this app is tailored to enhance your anime journey.

## Features

* **Search Functionality: Our intuitive search feature enables users to quickly find anime titles. The search function is designed to be user-friendly and responsive, ensuring that you can find exactly what you're looking for with minimal effort.**

* **Watchlist Management: With this feature, users can easily add anime titles to their watchlist. The watchlist is organized and accessible, making it simple to keep track of the anime you plan to watch later. The management tools provided help in organizing and sorting your list as needed.**
* **User-Friendly Interface: The application offers a straightforward and engaging user interface. Users can create an account, log in, search for anime, and add their favorite titles to the watchlist seamlessly. The interface is designed to be intuitive and easy to navigate, ensuring a smooth user experience.**

* **Account Management: Users can create an account, manage their profile, and update their information. The account management system is secure and designed to protect user data.**

## Tech Stack

* **Frontend: The frontend of the application is built using CSS and the Bootstrap framework. CSS provides the styling, while Bootstrap offers a responsive and modern design for various screen sizes. Bootstrap components are used for buttons, forms, and other UI elements to enhance user interaction.**

* **Backend: The backend is developed using Jinja and Flask. Jinja is a templating engine for Python that allows for dynamic content rendering, while Flask is a lightweight WSGI web application framework that serves as the backbone of the server-side logic.**

* **Database: The application uses SQLite3 as the database to store user information and anime watchlist data. SQLite3 is a lightweight and efficient database engine that integrates seamlessly with the application.**

## Technical Details

The Anime Watchlist Web App leverages the Jikan API (v4.0.0) for fetching anime data. Jikan is a RESTful API that does not require an API key, making it accessible for various applications. It allows users to retrieve comprehensive information about anime with simple HTTPS requests. The general format of the API request to search for anime by name is:


    https://api.jikan.moe/v4/anime?order_by=score&limit=25&sort=desc&sfw=true&q={Anime Title}

Here’s a breakdown of the query parameters used in the request:

* **order_by=score: Orders the results by the anime score from MyAnimeList (MAL). Other possible values include mal_id, title, start_date, end_date, episodes, scored_by, rank, popularity, members, or favorites.**

* **limit=25: Limits the number of search results to 25 for optimal performance.**

* **sort=desc: Sorts the results in descending order of the specified parameter. Change to asc for ascending order.**

* **sfw=true: Filters out not safe for work (NSFW) content. This parameter can be omitted if you prefer to include all content.**

The homepage of the application also features anime recommendations based on MAL data called forom jikan api with following https request.

    https://api.jikan.moe/v4/top/anime

For additional parameters and features of the Jikan API, refer to the Jikan API documentation.

User information and watchlist data are stored in an SQLite database. Passwords are securely encrypted using the werkzeug.security module in Python before being saved to the database. The anime watchlist is designed to minimize API calls by storing the anime name and image URL in the database. This approach improves performance but may occasionally result in image URLs becoming outdated. Users can resolve this issue by re-adding the anime to their watchlist.
The website uses CSS and the popular Bootstrap framework for its frontend design. Bootstrap’s components enhance the visual appeal and functionality of the site, while images used in the website are sourced from Pixelbay.
[picture link](https://cdn.pixabay.com/photo/2023/05/24/13/38/anime-8014848_1280.jpg)


## Database Schema
![structure of anime.db tables ](https://dl.imgdrop.io/file/aed8b140-8472-4813-922b-7ce35ef93c9e/2024/07/28/database_diagramac97fc8547da6bc8.png)

The application’s database, named anime.db, is located in the project folder and consists of two primary tables:

### 1. users: Contains user information with three columns:
* id: Primary key, a unique identifier for each user.
* user_name: The username of the user.
* hash: The hashed password for secure storage.

### 2. list: Stores watchlisted anime with three columns:
* user_id: Foreign key referencing the id in the users table.
* anime_name: The name of the anime.
* image_url: The URL of the anime’s image.

When a user decides to remove an anime from their watchlist, the corresponding entry is deleted from the database.

## Future Improvements

There are several enhancements planned for future versions of the app:

* Advanced Search Filters: Implement additional filters for search queries, such as genre, release year, and rating.
* User Reviews and Ratings: Allow users to leave reviews and rate anime titles.
* Enhanced Recommendations: Develop a recommendation system based on user preferences and viewing history.
* Mobile Optimization: Improve the mobile experience to ensure the app is fully functional and user-friendly on various devices.
