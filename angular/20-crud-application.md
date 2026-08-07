# Building a CRUD Application

Congratulations!

At this point, you've learned nearly all the core Angular concepts:

- Components
- Templates
- Data Binding
- Directives
- Services
- Dependency Injection
- Routing
- HttpClient
- RxJS
- Authentication
- Pipes
- Performance

Now it's time to put everything together by building a **real-world CRUD application**.

CRUD stands for

- **C**reate
- **R**ead
- **U**pdate
- **D**elete

This is one of the most common Angular interview topics because it demonstrates how multiple Angular concepts work
together.

______________________________________________________________________

# Application Overview

We'll build a simple

```
Employee Management System
```

Features

- Login
- Employee List
- Employee Details
- Add Employee
- Edit Employee
- Delete Employee
- Search Employees
- Pagination

______________________________________________________________________

# Architecture

```
Browser

↓

Angular

↓

Employee Component

↓

Employee Service

↓

HttpClient

↓

REST API

↓

Database
```

Everything you've learned so far comes together.

______________________________________________________________________

# Project Structure

```
src/

└── app/

    ├── core/

    ├── shared/

    ├── features/

    │   └── employees/

    │       ├── pages/

    │       ├── components/

    │       ├── services/

    │       ├── models/

    │       └── employees.routes.ts

    ├── app.routes.ts

    └── main.ts
```

______________________________________________________________________

# Employee Model

```typescript
export interface Employee {

    id: number;

    firstName: string;

    lastName: string;

    email: string;

    department: string;

    salary: number;

}
```

Always create interfaces.

______________________________________________________________________

# REST Endpoints

```
GET

/api/employees
```

```
GET

/api/employees/10
```

```
POST

/api/employees
```

```
PUT

/api/employees/10
```

```
DELETE

/api/employees/10
```

Standard REST API.

______________________________________________________________________

# Application Flow

```
User

↓

Employee List

↓

Employee Service

↓

Backend

↓

Database

↓

JSON

↓

Angular

↓

UI
```

______________________________________________________________________

# Employee Service

```typescript
@Injectable({

providedIn:"root"

})

export class EmployeeService {

constructor(

private http:

HttpClient

){}

}
```

______________________________________________________________________

# Get Employees

```typescript
getEmployees(){

return this.http.get<Employee[]>(

"/api/employees"

);

}
```

______________________________________________________________________

# Get Employee

```typescript
getEmployee(

id:number

){

return this.http.get<Employee>(

`/api/employees/${id}`

);

}
```

______________________________________________________________________

# Create Employee

```typescript
createEmployee(

employee:Employee

){

return this.http.post(

"/api/employees",

employee

);

}
```

______________________________________________________________________

# Update Employee

```typescript
updateEmployee(

id:number,

employee:Employee

){

return this.http.put(

`/api/employees/${id}`,

employee

);

}
```

______________________________________________________________________

# Delete Employee

```typescript
deleteEmployee(

id:number

){

return this.http.delete(

`/api/employees/${id}`

);

}
```

______________________________________________________________________

# Component

```
Employee List

↓

Calls Service

↓

Receives Observable

↓

Displays Employees
```

______________________________________________________________________

# Loading Employees

```typescript
ngOnInit(){

this.employeeService

.getEmployees()

.subscribe(

employees =>

this.employees = employees

);

}
```

______________________________________________________________________

# Template

```html
<table>

@for (

employee of employees;

track employee.id

){

<tr>

<td>

{{ employee.firstName }}

</td>

<td>

{{ employee.department }}

</td>

</tr>

}

</table>
```

______________________________________________________________________

# Loading State

Component

```typescript
loading = true;
```

Flow

```
API Starts

↓

Loading=true

↓

API Finished

↓

Loading=false
```

Template

```html
@if (loading) {

<p>

Loading...

</p>

}
```

______________________________________________________________________

# Error State

```
API

↓

Error

↓

Display Message
```

Example

```html
@if (errorMessage) {

<p>

{{ errorMessage }}

</p>

}
```

______________________________________________________________________

# Empty State

No employees?

```html
@if (

employees.length === 0

){

<p>

No Employees Found

</p>

}
```

Never leave users with a blank screen.

______________________________________________________________________

# Add Employee

Flow

```
User

↓

Form

↓

Submit

↓

POST

↓

Refresh List
```

______________________________________________________________________

# Edit Employee

```
Employee List

↓

Edit Button

↓

Load Employee

↓

Update Form

↓

PUT

↓

Refresh
```

______________________________________________________________________

# Delete Employee

```
Delete

↓

Confirmation

↓

DELETE

↓

Refresh List
```

Always confirm destructive actions.

______________________________________________________________________

# Search

User types

```
John
```

Flow

```
keyup

↓

debounceTime

↓

switchMap

↓

Backend

↓

Results
```

Avoid calling the API on every keystroke.

______________________________________________________________________

# Pagination

Instead of loading

```
10,000 Employees
```

Load

```
20

Per Page
```

Example

```
GET

/api/employees

?page=1

&size=20
```

______________________________________________________________________

# Sorting

```
Name

↓

Ascending

↓

Descending
```

Backend

usually handles sorting.

______________________________________________________________________

# Filtering

```
Department

↓

Engineering
```

Backend

returns

matching employees.

______________________________________________________________________

# Reactive Form

```
First Name

Last Name

Email

Department

Salary
```

Each field

is a

```
FormControl
```

We'll build

validation

using Reactive Forms.

______________________________________________________________________

# Validation

Required

```typescript
Validators.required
```

Email

```typescript
Validators.email
```

Salary

```typescript
Validators.min(0)
```

Prevent invalid requests.

______________________________________________________________________

# Disable Submit

```html
<button

[disabled]="form.invalid"

>

Save

</button>
```

______________________________________________________________________

# Success Message

```
Employee Created

✔ Success
```

Good UX

always informs

the user.

______________________________________________________________________

# Navigation

```
Employee List

↓

Employee Details

↓

Edit Employee

↓

Back
```

Use Angular Router.

______________________________________________________________________

# Authentication

Requests

```
Authorization

Bearer JWT
```

Automatically

added

by

```
Interceptor
```

______________________________________________________________________

# Loading Indicator

```
Button

↓

Spinner

↓

API

↓

Hide Spinner
```

Improves

user experience.

______________________________________________________________________

# Error Handling

```
400

↓

Validation Error
```

```
404

↓

Employee Not Found
```

```
500

↓

Server Error
```

Display

friendly messages.

______________________________________________________________________

# Folder Structure

```
employees/

├── pages/

│   ├── employee-list/

│   ├── employee-details/

│   └── employee-form/

├── components/

│   ├── employee-table/

│   ├── search-box/

│   └── employee-card/

├── services/

├── models/

└── employees.routes.ts
```

______________________________________________________________________

# Complete Request Flow

```
User Click

↓

Component

↓

Service

↓

HttpClient

↓

Interceptor

↓

Backend

↓

Database

↓

JSON

↓

Observable

↓

Component

↓

Template

↓

Browser
```

______________________________________________________________________

# Enterprise Enhancements

Real applications often include

- Server-side pagination
- Infinite scrolling
- Optimistic UI updates
- Audit logs
- Export to Excel
- Import from CSV
- Role-based permissions
- Soft delete
- Bulk operations

______________________________________________________________________

# Optimistic Update

Instead of waiting

```
Click Save

↓

Wait

↓

Update UI
```

Use

```
Click Save

↓

Update UI

↓

Backend

↓

Rollback If Failed
```

Better UX.

______________________________________________________________________

# Caching

Employee list

rarely changes.

```
API

↓

Cache

↓

Reuse
```

Reduces

network traffic.

______________________________________________________________________

# Common Mistakes

## API Calls Inside Templates

Wrong

```html
{{

loadUsers()

}}
```

Never call APIs

from templates.

______________________________________________________________________

## Huge Components

Split

```
Employee List

Search

Table

Pagination

Filters
```

into

multiple components.

______________________________________________________________________

## Ignoring Loading States

Always show

```
Loading...
```

while waiting

for backend responses.

______________________________________________________________________

## Forgetting Error Handling

Every API call

can fail.

Handle it gracefully.

______________________________________________________________________

## Not Using track

Always

```html
track employee.id
```

when rendering lists.

______________________________________________________________________

# Best Practices

✅ Keep components small.

✅ Keep API calls inside services.

✅ Use Reactive Forms.

✅ Validate user input.

✅ Handle loading, empty, and error states.

✅ Use pagination.

✅ Use AsyncPipe where appropriate.

✅ Keep project feature-based.

______________________________________________________________________

# Interview Deep Dive

## Question

What is CRUD?

### Answer

CRUD stands for Create, Read, Update, and Delete. These four operations form the foundation of most business
applications and correspond to HTTP methods such as POST, GET, PUT/PATCH, and DELETE.

______________________________________________________________________

## Question

Why should API calls be placed inside services?

### Answer

Services separate business logic and data access from the UI, making components simpler, easier to test, and more
reusable.

______________________________________________________________________

## Question

Why should Angular applications display loading and error states?

### Answer

Network requests take time and may fail. Showing loading indicators and meaningful error messages improves the user
experience and makes applications more robust.

______________________________________________________________________

## Question

Why is pagination important?

### Answer

Pagination reduces the amount of data transferred and rendered, improving backend performance, frontend performance, and
overall user experience.

______________________________________________________________________

## Question

Describe the complete CRUD request flow.

### Answer

A user interacts with a component, which calls a service. The service uses HttpClient to communicate with the backend
API. The backend processes the request and returns JSON. Angular receives the response, updates component state, and the
template automatically updates the UI.

______________________________________________________________________

# Practice Questions

1. What does CRUD stand for?
1. Which HTTP methods correspond to CRUD operations?
1. Why should services handle API communication?
1. Why should applications display loading states?
1. What are empty states?
1. Why is pagination important?
1. Why should forms be validated?
1. What is optimistic UI?
1. Why should API calls never be placed inside templates?
1. Explain the complete CRUD lifecycle from user action to database update.

______________________________________________________________________

# Summary

Building a CRUD application brings together nearly every core Angular concept you've learned.

In this chapter, you applied:

- Components
- Routing
- Services
- HttpClient
- RxJS
- Authentication
- Reactive Forms
- Validation
- Loading states
- Error handling
- Pagination
- Search
- CRUD operations
- Feature-based architecture
- Enterprise best practices

At this point, you have the knowledge to build a real-world Angular application. The remaining chapters focus on
interview preparation, modern Angular features, migration from legacy Angular, framework comparisons, and a backend
engineer's cheat sheet.

______________________________________________________________________

# Next

[Angular Interview Questions](21-angular-interview-questions.md)
