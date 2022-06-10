# `GET /aircraft` Returns an array of the aircraft in the database

#### Arguments:

`?page=` Page of aircraft to be returned. Defaults to 1.

`?limit=` Number of aircraft per page. Defaults to 100.

`?order=` Comma separated ordering/sorting specification of the aircraft. Categories: registration, manufacturer, icao_type, type, owner, category, and year_created. 
Defaults to registration.

Example: `GET /aircraft/?order=type,registration&year_created=2022&limit=3&page=5`
```json
[
    {
        "registration": "N928AK",
        "type": "737-9",
        "icao_type": "",
        "owner": "Alaska Airlines Inc",
        "category": "",
        "manufacturer": "Boeing",
        "year_created": 2022
    },
    {
        "registration": "N974AK",
        "type": "737-9",
        "icao_type": "",
        "owner": "Alaska Airlines Inc",
        "category": "",
        "manufacturer": "Boeing",
        "year_created": 2022
    },
    {
        "registration": "N632UP",
        "type": "747-8F",
        "icao_type": "",
        "owner": "United Parcel Service Co",
        "category": "",
        "manufacturer": "Boeing",
        "year_created": 2022
    }
]
```

`?search-<category>=` Only returns aircraft that contain the given value (Case Sensitive!) in the given category. Allowed categories are: type, icao_type, owner, category, "manufacturer, registration

Example: `GET /aircraft?search-owner=Delta&limit=2`
```json
[
  {
    "registration": "C-FAHO",
    "type": "204B (Bell)",
    "icao_type": "",
    "owner": "Delta Helicopters Ltd.",
    "category": "",
    "manufacturer": "Bell Helicopter Company",
    "year_created": null
  },
  {
    "registration": "C-FBHW",
    "type": "205A-1 (Bell)",
    "icao_type": "UH1",
    "owner": "Delta Helicopters Ltd.",
    "category": "",
    "manufacturer": "Bell Helicopter Textron Division Of Textron Inc.",
    "year_created": null
  }
]
```

`?registration=` Specify the registration of the aircraft. 

Example: `GET /aircraft?registration=N471MC&limit=1` 
```json
[
  {
    "registration": "N471MC", 
    "type": "747-412", 
    "icao_type": "", 
    "owner": "Bank Of Utah Trustee", 
    "category": "", 
    "manufacturer": "Boeing", 
    "year_created": 1997
  }
]
```

`?manufacturer=` Specify the manufacturer of the aircraft. 

Example: `GET /aircraft?manufacturer=Boeing&limit=1`
```json
[
   {
      "registration": " 98-6006",
      "type": "C-32B",
      "icao_type": "B752",
      "owner": "United States Air Force",
      "category": "No ADS-B Emitter Category Information",
      "manufacturer": "Boeing",
      "year_created": null
   },
   {
      "registration": "00-0171",
      "type": "C-17A Globemaster III",
      "icao_type": "C17",
      "owner": "United States Air Force",
      "category": "No ADS-B Emitter Category Information",
      "manufacturer": "Boeing",
      "year_created": null
   },
   {
      "registration": "00-0172",
      "type": "C-17A Globemaster III",
      "icao_type": "C17",
      "owner": "United States Air Force",
      "category": "No ADS-B Emitter Category Information",
      "manufacturer": "Boeing",
      "year_created": null
   }
]
```
`?icao_type=` Specify the [ICAO type code](https://en.wikipedia.org/wiki/List_of_aircraft_type_designators) of the aircraft.

Example: `GET /aircraft?icao_type=B763&limit=1`
```json
[
    {
        "registration": "2900",
        "type": "Boeing C-767",
        "icao_type": "B763",
        "owner": "Brazilian Air Force",
        "category": "",
        "manufacturer": "Boeing",
        "year_created": null
    }
]
```

`?type=` Specify the specific type of the aircraft.

Example: `GET /aircraft?type=767%203Q8ER&limit=2`
```json
[
    {
        "registration": "4X-EAM",
        "type": "767 3Q8ER",
        "icao_type": "B763",
        "owner": "El Al",
        "category": "No ADS-B Emitter Category Information",
        "manufacturer": "Boeing",
        "year_created": null
    },
    {
        "registration": "4X-EAN",
        "type": "767 3Q8ER",
        "icao_type": "B763",
        "owner": "El Al",
        "category": "No ADS-B Emitter Category Information",
        "manufacturer": "Boeing",
        "year_created": null
    }
]
```

`?owner=` Specify the name of the owner of the aircraft.

Example: `GET /aircraft/?owner=Delta%20Air%20Lines&limit=1`

```json
[
    {
        "registration": "N1402A",
        "type": "767 332",
        "icao_type": "B763",
        "owner": "Delta Air Lines",
        "category": "",
        "manufacturer": "Boeing",
        "year_created": null
    }
]
```

`?category=` Specify the [ICAO wake turbulence category](https://skybrary.aero/articles/icao-wake-turbulence-category) of the aircraft.

Example: `GET /aircraft/?category=Light%20(<%2015500%20lbs)&limit=1`
```json
[
    {
        "registration": "0169",
        "type": "Beech 1900 C-1",
        "icao_type": "B190",
        "owner": "Royal Thai Army",
        "category": "Light (< 15500 lbs)",
        "manufacturer": "Beech",
        "year_created": null
    }
]
```

`?year_created` Specify the year of creation of the aircraft.
Example: `GET /aircraft/?year_created=2022&limit=1`
```json
[
    {
        "registration": "N103DP",
        "type": "S2R-T660",
        "icao_type": "",
        "owner": "Thrush Aircraft Llc",
        "category": "",
        "manufacturer": "Thrush Aircraft Llc",
        "year_created": 2022
    }
]
```

# `POST /aircraft` Adds a new aircraft to the database

Example Body:
```json
{
    "type": "737-8CF",
    "icao_type": "B738",
    "owner": "YHDiamond",
    "category": "Light (< 15500 lbs)",
    "manufacturer": "Boeing",
    "registration": "PIZZA123",
    "year_created": 1993
}
```


# `GET /summary` Returns an object with statistics of the aircraft database 
Includes oldest and youngest aircraft, average aircraft age, and the total number of aircraft in the database

#### Arguments
`?most-<category>=` Specifies how much of the "ranking" of the most common item in that category that should be returned (and how many occurrences it has). Default 0 for all.

Example: `GET /summary?most-manufacturer=3`
```json
{
  "most_common": {
    "manufacturer": {
      "Cessna": 72598,
      "Piper": 44796,
      "Beech": 18484
    }
  },
  "avg_age": "40.2981453205480568",
  "total_aircraft": 432105,
  "oldest_aircraft": 1909,
  "youngest_aircraft": 2022
}
```

`?remove_empty=true` Specifies whether to remove empty string ("") and null values from the most common response. Defaults to false.