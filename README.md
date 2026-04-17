# Automated Report Generation & Distribution

## Project Overview
Automates scheduled data extraction, report creation, and email distribution. Built to save business hours on recurring analytics and improve data-driven communication.

## Features
- Pulls data from CSV/Excel/SQL/API
- Cleans and aggregates with pandas
- Generates Excel reports (with charts, stats)
- Automatically sends reports via email
- Scheduled and fully logged runs

## Quick Start

1. Clone this repo  
   `git clone https://github.com/B-313/report-scheduler.git`
2. Set up a Python environment and install requirements  
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in email credentials
4. Add your config in `config/config.yaml`
5. Run directly or use the built-in scheduler

## Sample Output

![Screenshot of report](output/screenshot.png)

## Configuration

- Edit `config/config.yaml` for preferences
- Add sample data to `/data`

## Contact

Questions? Raise an issue or connect via [LinkedIn](https://www.linkedin.com/in/bhanuja-kumar/).