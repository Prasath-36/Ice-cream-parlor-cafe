
# Ice Cream Parlor Management Application

## Overview
The **Ice Cream Parlor Management Application** is a GUI-based system built using Python's `tkinter` library. It allows users to manage a seasonal ice cream menu, a shopping cart for orders, and a list of allergens. The app is backed by an SQLite database for data persistence.

---

## Features
1. **Seasonal Flavors Management**
   - Add new ice cream flavors with name, description, and price.
   - Search for specific flavors by name.
   - Delete flavors from the menu.

2. **Shopping Cart**
   - Add selected flavors to the cart.
   - View cart items, including quantity and total value.
   - Remove items from the cart.

3. **Allergens Management**
   - Add allergens to a dedicated list.
   - Delete allergens from the list.

4. **Data Persistence**
   - All data (flavors, cart items, and allergens) is stored in an SQLite database.

---

## Prerequisites
- Python 3.x
- SQLite3 (included with Python)
- `tkinter` (included with Python)

---

## Project Structure
- **`ice_cream.db`**: SQLite database created automatically for storing data.
- **`IceCreamApp` class**: The main GUI class for the application.
- **Database tables**:
  - `seasonal_flavors`: Stores ice cream flavor details.
  - `cart`: Stores items added to the cart.
  - `allergens`: Stores allergen information.

---

## How to Run
1. Clone or download this repository to your local machine.
2. Ensure Python 3 is installed on your system.
3. Run the application using the command:
   ```bash
   python main.py
   ```
4. The GUI will open, and you can start managing your ice cream parlor data.

---
## Run the Application with Docker

1. **Build the Docker Image**:
   ```bash
   docker build -t ice-cream-app .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d --name ice-cream-app-container -p 8000:8000 ice-cream-app
   ```

   - Replace `8000:8000` with the appropriate port mapping if your application uses a different port.

3. **Stop the Docker Container**:
   ```bash
   docker stop ice-cream-app-container
   ```

4. **Remove the Docker Container**:
   ```bash
   docker rm ice-cream-app-container
   ```

5. **Remove the Docker Image**:
   ```bash
   docker rmi ice-cream-app
   ```

---

## Database Tables and Functions

### Tables
1. **`seasonal_flavors`**:
   - Columns: `id`, `name`, `description`, `price`

2. **`cart`**:
   - Columns: `id`, `flavor_id`, `quantity`
   - Linked to `seasonal_flavors` via `flavor_id`.

3. **`allergens`**:
   - Columns: `id`, `name`

### Functions
- **Database Initialization**: `init_db()`
  - Creates tables if they don’t exist.
- **ID Reset**: `reset_ids(table_name)`
  - Resets auto-incrementing IDs for a specified table.
- **CRUD Operations**:
  - Add flavors, allergens, and cart items.
  - Remove items or search for flavors.

---

## GUI Layout
### Tabs
1. **Seasonal Flavors**
   - Input fields for adding new flavors.
   - Search functionality for flavors.
   - Display of all flavors in a table.
   - Buttons to add flavors to the cart or delete them.

2. **Cart**
   - Display of cart items in a table.
   - Button to remove items from the cart.
   - Total cart value displayed at the bottom.

3. **Allergens**
   - Input field for adding allergens.
   - Display of allergens in a table.
   - Button to delete allergens.

---

## Future Enhancements
- Implement user authentication.
- Add support for exporting cart data as a receipt.
- Include options to update flavor details.
- Add a summary report for allergens and flavor popularity.

---



