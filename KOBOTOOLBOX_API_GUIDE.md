# Cowsville API Documentation for KoboToolbox Integration

## Base URL

```
http://78.47.170.156/api/
```

## Authentication

All endpoints require authentication. Include token in headers:

```
Authorization: Token <your-auth-token>
Content-Type: application/json
```

---

# Farm Endpoints

## 1. Create Farm

**Endpoint:** `POST /farms/`

**Purpose:** Register a new farm in the system

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Unique farm identifier | `"FARM001"` |
| `owner_name` | String | Farm owner's name | `"John Doe"` |
| `address` | String | Farm location | `"Addis Ababa, Ethiopia"` |

**Optional Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tel_no` | String | Phone number (will be formatted) | `"0912345678"` |
| `location_gps` | String | GPS coordinates | `"9.03, 38.74"` |
| `cluster_number` | String | Cluster ID | `"C001"` |
| `fcc_no` | Integer | Fertility camp number | `1` |
| `herd_size` | Integer | Total number of cows | `50` |
| `calves` | Integer | Number of calves | `10` |
| `milking_cows` | Integer | Number of milking cows | `30` |
| `TDM` | Float | Total daily milk (liters) | `250.5` |
| `housing` | String | Type of housing | `"free_stall"` or `"tie_stall"` |
| ` floor` | String | Floor type | `"concrete"` or `"earth"` |
| `feed` | String | Main feed type | `"hay"` or `"grass"` |
| `feeding_rate` | String | Feeding frequency | `"twice_a_day"` |
| `water_source` | String | Water source type | `"tap_water"` or `"well"` |
| `water_rate` | String | Watering frequency | `"twice_a_day"` |
| `hygiene_score` | String | Hygiene rating | `"good"` or `"fair"` or `"poor"` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "owner_name": "John Doe",
  "address": "Addis Ababa",
  "tel_no": "0912345678",
  "herd_size": "50",
  "calves": "10",
  "milking_cows": "30",
  "TDM": "250.5",
  "housing": "free_stall",
  "floor": "concrete",
  "feed": "hay",
  "feeding_rate": "twice_a_day",
  "water_source": "tap_water",
  "hygiene_score": "good"
}
```

**Success Response (201 Created):**

```json
{
  "farm_id": "FARM001",
  "owner_name": "John Doe",
  "telephone_number": "+251912345678",
  "total_number_of_cows": 50,
  ...
}
```

---

## 2. Update Farm

**Endpoint:** `PUT/PATCH /farms/{id}/`

Same fields as Create Farm, all optional for PATCH

---

## 3. Change Farm Inseminator

**Endpoint:** `POST /farms/{id}/change_inseminator/`

**Purpose:** Assign/change inseminator for a farm

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `inseminator_id` | Integer | ID of the inseminator (use `staff_id`) | `1` |

**Example Request:**

```json
{
  "staff_id": 1
}
```

---

## 4. Change Farm Doctor

**Endpoint:** `POST /farms/{id}/change_doctor/`

**Purpose:** Assign/change doctor for a farm

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `doctor_id` | Integer | ID of the doctor (use `staff_id`) | `2` |

**Example Request:**

```json
{
  "staff_id": 2
}
```

---

# Cow Endpoints

## 1. Create Cow

**Endpoint:** `POST /cows/`

**Purpose:** Register a new cow in the system

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id_input` | String | Farm identifier | `"FARM001"` |
| `cow_id_input` | String | Unique cow identifier | `"COW-101"` |
| `breed` | String | Breed name | `"holstein"` or `"jersey"` |
| `date_of_birth` | Date | Birth date | `"2020-01-15"` |
| `sex` | String | Cow gender | `"female"` or `"male"` |

**Optional Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `parity` | Integer | Number of births | `2` |
| `body_weight` | Float | Weight in kg | `450.5` |
| `bcs` | String/Float | Body condition score (1-5) | `"3.5"` |
| `gynecological_status_name` | String | Reproductive status | `"open"` or `"pregnant"` |
| `lactation_number` | Integer | Current lactation number | `2` |
| `days_in_milk` | Integer | Days since calving | `120` |
| `average_daily_milk` | Float | Daily milk production (L) | `25.5` |
| `cow_inseminated_before` | String | Has been inseminated? | `"yes"` or `"no"` |
| `last_date_insemination` | Date | Last insemination date | `"2023-05-15"` |
| `number_of_inseminations` | Integer | Total inseminations | `3` |
| `id_or_breed_bull_used` | String | Bull breed/ID used | `"Holstein Bull #123"` |
| `last_calving_date` | Date | Last birth date | `"2022-12-10"` |
| `has_lameness` | String | Is lame? | `"yes"` or `"no"` |
| `is_vaccinated` | String | Vaccinated? | `"yes"` or `"no"` |
| `vaccination_date` | Date | Vaccination date | `"2023-01-15"` |
| `vaccination_type` | String | Vaccine type | `"FMD, Anthrax"` |
| `deworming` | String | Dewormed? | `"yes"` or `"no"` |
| `deworming_date` | Date | Deworming date | `"2023-02-01"` |
| `deworming_type` | String | Dewormer used | `"Ivermectin"` |
| `is_pregnant` | String | Currently pregnant? | `"yes"` or `"no"` |
| `heat_start_date` | DateTime | Last heat date | `"2023-06-01T08:00:00"` |
| `heat_signs` | String | Heat signs observed | `"mounting, mucus"` |

**Example Request:**

```json
{
  "farm_id_input": "FARM001",
  "cow_id_input": "COW-101",
  "breed": "holstein",
  "date_of_birth": "2020-01-15",
  "sex": "female",
  "parity": 2,
  "body_weight": 450.5,
  "bcs": "3.5",
  "lactation_number": 2,
  "days_in_milk": 120,
  "average_daily_milk": 25.5,
  "has_lameness": "no",
  "is_vaccinated": "yes",
  "vaccination_date": "2023-01-15",
  "vaccination_type": "FMD, Anthrax"
}
```

---

## 2. Get Cows by Farm

**Endpoint:** `GET /cows/by_farm/?farm_id={farm_id}`

**Purpose:** List all cows in a specific farm

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `farm_id` | String | Yes | Farm identifier |

**Example Request:**

```
GET /api/cows/by_farm/?farm_id=FARM001
```

---

## 3. Record Heat Sign

**Endpoint:** `POST /cows/record_heat_sign/`

**Purpose:** Record when a cow shows heat signs

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `heat_start_time` | DateTime | When heat started | `"2023-06-01T08:00:00"` |

**Optional Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `heat_signs` | String | Signs observed | `"mounting, mucus discharge"` |
| `heat_sign_recorded_at` | DateTime | When recorded | `"2023-06-01T09:00:00"` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "heat_start_time": "2023-06-01T08:00:00",
  "heat_signs": "mounting, mucus discharge"
}
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "message": "Heat sign recorded successfully",
  "data": {
    "cow_id": "COW-101",
    "farm_id": "FARM001",
    "heat_sign_start": "2023-06-01T08:00:00Z",
    "notifications_sent": {...}
  }
}
```

---

## 4. Monitor Pregnancy

**Endpoint:** `POST /cows/monitor_pregnancy/`

**Purpose:** Record pregnancy confirmation

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `pregnancy_date` | Date | Pregnancy diagnosis date | `"2023-07-15"` |
| `days_until_calving` | Integer | Days until expected calving | `280` |
| `service_per_conception` | Integer | Services needed to conceive | `2` |
| `lactation_number` | Integer | Current lactation | `3` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "pregnancy_date": "2023-07-15",
  "days_until_calving": 280,
  "service_per_conception": 2,
  "lactation_number": 3
}
```

---

## 5. Farmer Medical Assessment

**Endpoint:** `POST /cows/farmer_medical_assessment/`

**Purpose:** Farmer reports cow sickness

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `sickness_description` | String | Symptoms description | `"Reduced appetite and lethargy"` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "sickness_description": "The cow has reduced appetite, is not eating well, and appears lethargic. Also noticed some discharge."
}
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "message": "Medical assessment submitted successfully",
  "data": {
    "report_id": 42,
    "farm_id": "FARM001",
    "cow_id": "COW-101",
    "reported_date": "2023-07-20T10:30:00Z"
  }
}
```

**Requirements:**

- Farm MUST have a doctor assigned
- Sends SMS to doctor
- Sends confirmation SMS to farmer

---

## 6. Doctor Medical Assessment

**Endpoint:** `POST /cows/doctor_assessment/`

**Purpose:** Doctor records medical examination results

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `doctor_id` | Integer | Doctor's ID | `2` |
| `is_cow_sick` | Boolean | Is the cow sick? | `true` or `false` |

**Optional Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `general_health` | Integer/String | General health status ID or name | `1` or `"normal"` |
| `udder_health` | Integer/String | Udder health status ID or name | `4` or `"1qt_normal"` |
| `mastitis` | Integer/String | Mastitis status ID or name | `1` or `"negative"` |
| `has_lameness` | Boolean | Has lameness? | `true` or `false` |
| `body_condition_score` | Float | BCS (1-5) | `3.5` |
| `reproductive_health` | String | Reproductive status | `"Normal"` or `"Abnormal"` |
| `metabolic_disease` | String | Metabolic status | `"Normal"` |
| `is_cow_vaccinated` | Boolean | Vaccinated? | `true` or `false` |
| `vaccination_date` | Date | Vaccination date | `"2023-01-15"` |
| `vaccination_type` | String | Vaccine type | `"FMD"` |
| `has_deworming` | Boolean | Dewormed? | `true` or `false` |
| `deworming_date` | Date | Deworming date | `"2023-02-01"` |
| `deworming_type` | String | Dewormer used | `"Ivermectin"` |
| `diagnosis` | String | Diagnosis | `"Clinical mastitis"` |
| `treatment` | String | Treatment given | `"Antibiotics"` |
| `prescription` | String | Prescription | `"Continue treatment for 5 days"` |
| `notes` | String | Additional notes | `"Follow-up in 1 week"` |

**Valid Health Status Values:**

**Udder Health:**

- `"1qt_normal"` (ID: 4)
- `"2qt_normal"` (ID: 3)
- `"3qt_normal"` (ID: 2)
- `"4qt_normal"` (ID: 1)

**Mastitis:**

- `"negative"` (ID: 1)
- `"clinical_mastitis"` (ID: 2)
- `"cmt_plus"` (ID: 3) - CMT +
- `"cmt_plus_plus"` (ID: 4) - CMT ++
- `"cmt_plus_plus_plus"` (ID: 5) - CMT +++

**General Health:**

- `"normal"` (ID: 1)
- `"sick"` (ID: 2)

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "doctor_id": 2,
  "is_cow_sick": true,
  "general_health": "sick",
  "udder_health": "1qt_normal",
  "mastitis": "cmt_plus",
  "has_lameness": false,
  "body_condition_score": 3.0,
  "diagnosis": "Clinical mastitis in one quarter",
  "treatment": "Intramammary antibiotics",
  "prescription": "Apply antibiotics twice daily for 5 days",
  "notes": "Monitor milk production. Follow-up in 1 week."
}
```

---

## 7. Monitor Heat Sign

**Endpoint:** `POST /cows/monitor_heat_sign/`

**Purpose:** Record insemination after heat detection

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `is_inseminated` | Boolean | Was inseminated? | `true` or `false` |
| `insemination_count` | Integer | Service number | `1` |
| `lactation_number` | Integer | Current lactation | `2` |

**Optional Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `date_of_insemination` | Date | Insemination date | `"2023-06-02"` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "is_inseminated": true,
  "insemination_count": 1,
  "lactation_number": 2,
  "date_of_insemination": "2023-06-02"
}
```

---

## 8. Monitor Birth

**Endpoint:** `POST /cows/monitor_birth/`

**Purpose:** Record calving event

**Required Fields:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `farm_id` | String | Farm identifier | `"FARM001"` |
| `cow_id` | String | Cow identifier | `"COW-101"` |
| `calving_date` | Date | Date cow gave birth | `"2023-12-15"` |
| `last_calving_date` | Date | Same as calving_date | `"2023-12-15"` |
| `calf_sex` | String | Calf gender | `"male"` or `"female"` |

**Example Request:**

```json
{
  "farm_id": "FARM001",
  "cow_id": "COW-101",
  "calving_date": "2023-12-15",
  "last_calving_date": "2023-12-15",
  "calf_sex": "female"
}
```

---

## 9. Get Pregnancy Records

**Endpoint:** `GET /cows/pregnancy_records/?farm_id={farm_id}`

**Purpose:** Get all pregnant cows records

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `farm_id` | String | Yes | Farm identifier |
| `cow_id` | String | No | Specific cow ID |

---

## 10. Get Birth Records

**Endpoint:** `GET /cows/birth_records/?farm_id={farm_id}`

**Purpose:** Get all birth records

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `farm_id` | String | Yes | Farm identifier |
| `cow_id` | String | No | Specific cow ID |

---

## 11. Get Heat Sign Records

**Endpoint:** `GET /cows/heat_sign_records/?farm_id={farm_id}`

**Purpose:** Get heat sign records

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `farm_id` | String | Yes | Farm identifier |
| `cow_id` | String | No | Specific cow ID |
| `record_type` | String | No | `"all"`, `"reproduction"`, or `"insemination"` |

---

# Error Responses

**Validation Error (400 Bad Request):**

```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

**Not Found (404):**

```json
{
  "detail": "Not found."
}
```

**Server Error (500):**

```json
{
  "error": "Error message description"
}
```

---

# Important Notes for KoboToolbox Integration

## 1. Field Mapping

- KoboToolbox field names should match the API field names exactly
- For boolean fields: use `"yes"` / `"no"` (will be converted automatically)
- For dates: use format `YYYY-MM-DD` (e.g., `2023-06-15`)
- For datetimes: use format `YYYY-MM-DDTHH:MM:SS` (e.g., `2023-06-15T08:30:00`)

## 2. Farm Prerequisites

- Farms must have inseminators assigned before recording heat/insemination
- Farms must have doctors assigned before farmer medical assessments

## 3. Choice Fields (Use exact values)

**Breeds:** Check available breeds in system
**Housing Types:** `free_stall`, `tie_stall`, etc.
**Floor Types:** `concrete`, `earth`, etc.
**Feeding Rates:** `once_a_day`, `twice_a_day`, `three_times_a_day`
**Water Sources:** `tap_water`, `well`, `river`, etc.

## 4. Status Values (Use underscores, not spaces)

- ❌ Wrong: `"1qt normal"`, `"cmt3"`
- ✅ Correct: `"1qt_normal"`, `"cmt_plus_plus"`

## 5. Phone Number Format

- Input: `"0912345678"`
- API converts to: `"+251912345678"`
- Both Ethiopian formats accepted

## 6. Notifications

The system automatically sends SMS notifications for:

- Heat sign recording (to inseminator)
- Pregnancy confirmation (to farmer)
- Medical reports (to doctor and farmer)
- Birth events (to farmer)

---

# Quick Reference Checklist

### Creating a Farm from KoboToolbox:

- [ ] `farm_id` (required)
- [ ] `owner_name` (required)
- [ ] `address` (required)
- [ ] `tel_no` (optional but recommended)
- [ ] Numeric fields can be strings (will convert)
- [ ] Choice fields should match system values

### Creating a Cow from KoboToolbox:

- [ ] `farm_id_input` (required - must exist)
- [ ] `cow_id_input` (required - unique)
- [ ] `breed` (required - must match breed name)
- [ ] `date_of_birth` (required)
- [ ] `sex` (required - "male" or "female")
- [ ] Yes/no fields: use `"yes"` or `"no"`

### Recording Heat Sign:

- [ ] `farm_id`, `cow_id` (required)
- [ ] `heat_start_time` (required - datetime)
- [ ] Farm must have active inseminator

### Doctor Assessment:

- [ ] Use exact status names with underscores
- [ ] Check valid values before submitting
- [ ] Farm must have doctor assigned

---

**Last Updated:** November 27, 2025  
**API Version:** 1.0  
**Base URL:** http://78.47.170.156/api/
