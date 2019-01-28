# LINDA

## Installation Instructions
1. Execute Linda.py as often as you want.
	- e.g.: using a cronjob every minute
	- Linda generates logging output. Be sure to reroute it to something useful or to a null device
2.	Setup the Services using LindaSetup.py
	- Linda will guide you through the process.
3. Configfile anpassen:
	- Datei `configsample.ini` in `lindaconfig.ini` umbenennen.
	- Korrekte Daten eintragen
	
## CHANGELOG
### Version 0.1
- Existing Triggers:
	- DeviationTriggerTwoThresholds
- Existing Actions:
	- MailAction