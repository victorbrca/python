RHQ
================

Python scripts for enabling and disabling alert definitions in JBOSS Operations Network (JON/RHQ).

Identify all alert definitions ID and add it to a dictionary in the script named `alerts`. The first field is not relevant and is only used for the output.

```python
# Use a dictionary list of alerts by 'name':id
alerts = {
    'memory':10435,
    'cpu':10423,
}
```

Example output:

```bash
Disabling alert memory (ID: 10443)
                                    \- disabled

Disabling alert CPU (ID: 10471)
                                    \- disabled

Disabling alert Network connection (ID: 10425)
                                    \- disabled
```