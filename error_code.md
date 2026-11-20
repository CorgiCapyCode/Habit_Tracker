# Error Codes

| Code | Level | Message |
| --- | --- | --- |
| 0 | Success | Habit successfully added to the database. |
| 1 | Error | A habit with this name already exists. |
| 100 | Warning | Name was converted to a string. |
| 101 | Warning | Description was converted to a string. |
| 112 | Error | Active status was not a boolean. No data added. |
| 113 | Error | Periodicity was not an integer. No data added. |
| 114 | Error | Name cannot be None or empty. |
| 120 | Error | Standard periodicity does not contain only integers. |
| 121 | Error | Standard active status does not contain only booleans. |
| 122 | Error | Standard lists have different lengths. |
| 123 | Error | Not all inputs are lists. |
| 200 | Error | Habit tracking status cannot be changed; habit is marked as passive. |
| 201 | Warning | Habit already marked as complete for this due date. |
| 301 | Success | Name of habit changed. |
| 302 | Success | Description of habit changed. |
| 303 | Success | Periodicity of habit changed. |
| 304 | Success | Active status of habit changed. |
| 401 | Warning | No name changed. |
| 402 | Warning | No description changed. |
| 403 | Warning | No periodicity changed. |
| 404 | Warning | No active status changed. |
| 411 | Warning | Description is None. Set to default. |
| 412 | Warning | Periodicity is None or empty. Set to default 1. |
| 413 | Warning | Active status is None or empty. Set to default False. |
