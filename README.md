# IxLicensesMonitorNotifier

This Python script would pull license details from Ixia chassis and categorize licenses into buckets of

- Expired Licenses
- Licenses Expiring in 7 - 15 days
- Licenses Expiring in 15 - 30 days
- Licenses Expiring in 30 - 60 days
- Licenses Expiring in 60 - 180 days

How to use the tool

-  Git clone `https://github.com/ashwinjo/IxLicensesMonitorNotifier.git`  repository onto your local machine
-  Modify email_config.py file and enter your SMTP credentials
-  Modify config.py file and enter ixia chassis / username / password.
-  Modify config.py file to enter Polling Interval for report generation.
-  Run `pip install -r requirements.txt`
-  Run the python scipt as below.

```python
To https://github.com/ashwinjo/IxLicensesMonitorNotifier.git
(base) ashwjosh@C0HD4NKHCX IxLicensesMonitorNotifier % python licenseExpirationTracker.py
Polling for async operation ...
Completed async operation
Polling for async operation ...
Completed async operation
Polling for async operation ...
Completed async operation
Email sent successfully!
```


<img width="1425" alt="image" src="https://github.com/ashwinjo/IxLicensesMonitorNotifier/assets/120066169/00f3af8d-2b6e-4c93-b1d7-7ca571578a75">
