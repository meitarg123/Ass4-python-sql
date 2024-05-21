# SARS-CoV-2 Vaccine Distribution Center

This repository contains a Python and SQL-based implementation of a database system for managing a SARS-CoV-2 vaccine distribution center. The project was developed as part of the SPL211 course (Assignment 4).

## Assignment Overview

- **Create and Populate Database**: Setup and populate an SQL database from a configuration file (`config.txt`).
- **Process Orders**: Execute a list of orders from an orders file (`orders.txt`) to receive shipments and send vaccine doses to clinics.
- **Generate Summary**: Output a summary file (`output.txt`) that records the total inventory, demand, received shipments, and sent shipments after each order.

## Files

- **`main.py`**: Main script to run the application.
- **`dao.py`**: Contains the Data Access Object (DAO) classes for database interaction.
- **`dto.py`**: Contains the Data Transfer Object (DTO) classes for data representation.
- **`repository.py`**: Manages the repository and provides methods for processing orders and generating summaries.
