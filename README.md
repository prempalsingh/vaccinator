# Vaccinator
Quick script to check for COVID-19 vaccine availability in my area and send a notification when slots are available using Co-Win public APIs.

## Issues
1. Although the cron is set to run every 5 minutes, Github Actions is scheduling it with some random delay.
2. Looks like Co-Win has configured Cloudfront to block any requests originating from Github Actions runners. For now, setting up the cron on my own server.
