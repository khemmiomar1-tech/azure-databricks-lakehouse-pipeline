# Power BI - DAX Measures (Gold API Records)

```dax
Nb Records = COUNTROWS ( gold_api_records )
```

```dax
Records Updated Today =
CALCULATE (
    COUNTROWS ( gold_api_records ),
    gold_api_records[updated_at] >= TODAY ()
)
```

```dax
Distinct Contacts = DISTINCTCOUNT ( gold_api_records[email] )
```
