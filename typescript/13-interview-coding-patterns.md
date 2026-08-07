# Common Interview Coding Patterns

Knowing TypeScript syntax is only half the battle.

In interviews, you'll often be asked to manipulate:

- Arrays
- Objects
- API responses
- Nested data
- Maps
- Sets

The focus is usually on writing **clean, readable, and efficient code** rather than memorizing algorithms.

This chapter covers the coding patterns you are most likely to encounter in backend TypeScript interviews.

______________________________________________________________________

# Sample Data

We'll use the following data throughout the chapter.

```typescript
interface User {

    id: number;

    name: string;

    age: number;

    department: string;

    active: boolean;

}

const users: User[] = [

    {

        id: 1,

        name: "Alice",

        age: 25,

        department: "Engineering",

        active: true

    },

    {

        id: 2,

        name: "Bob",

        age: 31,

        department: "HR",

        active: false

    },

    {

        id: 3,

        name: "Charlie",

        age: 28,

        department: "Engineering",

        active: true

    }

];
```

______________________________________________________________________

# Filter Data

Find active users.

```typescript
const activeUsers =

users.filter(

    user => user.active

);
```

______________________________________________________________________

Find users older than 30.

```typescript
const seniorUsers =

users.filter(

    user => user.age > 30

);
```

______________________________________________________________________

# Map Data

Return only names.

```typescript
const names =

users.map(

    user => user.name

);
```

Output

```typescript
["Alice", "Bob", "Charlie"]
```

______________________________________________________________________

Create lightweight DTOs.

```typescript
const summaries =

users.map(user => ({

    id: user.id,

    name: user.name

}));
```

______________________________________________________________________

# Find One Item

```typescript
const user =

users.find(

    user => user.id === 2

);
```

Returns

```
Bob
```

or

```
undefined
```

______________________________________________________________________

# Check Existence

Using `some()`

```typescript
const exists =

users.some(

    user => user.name === "Alice"

);
```

Result

```
true
```

______________________________________________________________________

Using `every()`

```typescript
const allActive =

users.every(

    user => user.active

);
```

______________________________________________________________________

# Reduce

Count users.

```typescript
const total =

users.reduce(

    count => count + 1,

    0

);
```

______________________________________________________________________

Calculate total age.

```typescript
const totalAge =

users.reduce(

(

    total,

    user

) => total + user.age,

0

);
```

______________________________________________________________________

Average age.

```typescript
const averageAge =

totalAge /

users.length;
```

______________________________________________________________________

# Group By Department

Very common interview question.

```typescript
const grouped =

users.reduce(

(

    result,

    user

) => {

    result[

        user.department

    ] ??= [];

    result[

        user.department

    ].push(user);

    return result;

},

{} as Record<

string,

User[]

>

);
```

Result

```text
Engineering

↓

Alice

Charlie

HR

↓

Bob
```

______________________________________________________________________

# Count by Department

```typescript
const counts =

users.reduce(

(

    result,

    user

) => {

    result[

        user.department

    ] =

    (

        result[

            user.department

        ] ?? 0

    ) + 1;

    return result;

},

{} as Record<

string,

number

>

);
```

Output

```typescript
{

Engineering:2,

HR:1

}
```

______________________________________________________________________

# Remove Duplicates

Numbers

```typescript
const numbers =

[

1,

2,

2,

3,

3,

4

];

const unique =

[

...new Set(numbers)

];
```

Output

```typescript
[1,2,3,4]
```

______________________________________________________________________

Objects

```typescript
const uniqueUsers =

Array.from(

new Map(

users.map(

user => [

user.id,

user

]

)

).values()

);
```

______________________________________________________________________

# Sort

Ascending

```typescript
users.sort(

(

a,

b

) =>

a.age - b.age

);
```

Descending

```typescript
users.sort(

(

a,

b

) =>

b.age - a.age

);
```

______________________________________________________________________

Alphabetical

```typescript
users.sort(

(

a,

b

)=>

a.name.localeCompare(

b.name

)

);
```

______________________________________________________________________

# Flatten Arrays

Nested

```typescript
const data = [

[1,2],

[3,4],

[5]

];
```

Flatten

```typescript
const result =

data.flat();
```

Output

```typescript
[1,2,3,4,5]
```

______________________________________________________________________

Using `flatMap()`

```typescript
const words =

["Hello World"];

const letters =

words.flatMap(

word =>

word.split(" ")

);
```

______________________________________________________________________

# Convert Array to Map

```typescript
const userMap =

new Map(

users.map(

user => [

user.id,

user

]

)

);
```

Lookup

```typescript
userMap.get(2);
```

O(1)

______________________________________________________________________

# Lookup Object

```typescript
const lookup =

users.reduce(

(

result,

user

)=>{

result[

user.id

]=user;

return result;

},

{} as Record<

number,

User

>

);
```

______________________________________________________________________

# Merge Objects

```typescript
const employee = {

id:1,

name:"Alice"

};

const address = {

city:"Bangalore"

};

const merged = {

...employee,

...address

};
```

______________________________________________________________________

# Merge Arrays

```typescript
const all = [

...array1,

...array2

];
```

______________________________________________________________________

# Deep Copy

Avoid

```typescript
const copy =

original;
```

Both variables reference the same object.

______________________________________________________________________

Shallow Copy

```typescript
const copy = {

...original

};
```

______________________________________________________________________

Deep Copy

```typescript
const copy =

structuredClone(

original

);
```

For older environments, libraries like Lodash (`cloneDeep`) are commonly used.

______________________________________________________________________

# Remove Properties

```typescript
const {

password,

...publicUser

} = user;
```

Very common for API responses.

______________________________________________________________________

# Optional Chaining

```typescript
const city =

user?.address?.city;
```

Avoids runtime errors.

______________________________________________________________________

# Nullish Coalescing

```typescript
const city =

user.city

??

"Unknown";
```

______________________________________________________________________

# Safe Parsing

```typescript
function parse(

json: string

){

try{

return JSON.parse(

json

);

}

catch{

return null;

}

}
```

______________________________________________________________________

# Transform API Response

Suppose

```typescript
const response =

[

{

id:1,

firstName:"Alice",

lastName:"Smith"

}

];
```

Convert

```typescript
const users =

response.map(

user => ({

id:user.id,

name:

`${user.firstName}

${user.lastName}`

})

);
```

______________________________________________________________________

# Pagination

```typescript
const page = 2;

const size = 10;

const result =

users.slice(

(page-1)*size,

page*size

);
```

______________________________________________________________________

# Search

```typescript
const result =

users.filter(

user =>

user.name

.toLowerCase()

.includes(

"ali"

)

);
```

______________________________________________________________________

# Build Lookup Table

```typescript
const lookup =

Object.fromEntries(

users.map(

user => [

user.id,

user

]

)

);
```

Now

```typescript
lookup[2]
```

is O(1).

______________________________________________________________________

# Async Mapping

Wrong

```typescript
const result =

users.map(

async user =>

getOrders(

user.id

)

);
```

Returns

```
Promise[]
```

Correct

```typescript
const result =

await Promise.all(

users.map(

user =>

getOrders(

user.id

)

)

);
```

Very common interview question.

______________________________________________________________________

# Common Mistakes

## Forgetting map Returns New Array

Wrong

```typescript
map()

changes array
```

It doesn't.

______________________________________________________________________

## Using for Loop Everywhere

Modern TypeScript prefers

- map
- filter
- reduce
- find

when appropriate.

______________________________________________________________________

## Using sort Without Comparator

Wrong

```typescript
numbers.sort();
```

Correct

```typescript
numbers.sort(

(a,b)=>a-b

);
```

______________________________________________________________________

## Forgetting Promise.all()

Wrong

```typescript
users.map(

async ...

)
```

Always await the resulting promises.

______________________________________________________________________

# Best Practices

✅ Use `map()` for transformations.

✅ Use `filter()` for selection.

✅ Use `find()` when only one item is needed.

✅ Use `reduce()` for aggregation and grouping.

✅ Prefer immutable updates using the spread operator.

✅ Use `Map` for fast lookups.

✅ Handle async collections with `Promise.all()`.

______________________________________________________________________

# Interview Deep Dive

## Question

When should you use `map()` instead of `forEach()`?

### Answer

Use `map()` when you want to transform every element and return a new array. Use `forEach()` when performing side
effects, such as logging or updating external state, without producing a new array.

______________________________________________________________________

## Question

Why is `reduce()` considered powerful?

### Answer

`reduce()` can aggregate data into a single value or structure, making it useful for calculations, grouping, counting,
building lookup tables, and many other collection transformations.

______________________________________________________________________

## Question

Why should `Promise.all()` be used with `map(async ...)`?

### Answer

An `async` callback passed to `map()` returns an array of Promises. `Promise.all()` waits for all of those Promises to
resolve and returns their results, enabling concurrent execution.

______________________________________________________________________

## Question

How can duplicate objects be removed from an array?

### Answer

A common approach is to build a `Map` using a unique property such as `id` as the key and then return the map's values.
This keeps only one object per unique key.

______________________________________________________________________

## Question

How should sensitive fields be removed before returning an API response?

### Answer

Use object destructuring with the rest operator to exclude sensitive properties, such as passwords, while keeping the
remaining fields in a new object.

______________________________________________________________________

# Practice Questions

1. What is the difference between `map()` and `forEach()`?
1. When should `reduce()` be used?
1. How do you group data by a property?
1. How do you remove duplicate objects?
1. How do you safely perform asynchronous mapping?
1. How do you build a lookup table?
1. How do you paginate an array?
1. How do you remove properties from an object?
1. What is the difference between shallow and deep copy?
1. Why is `Map` useful for lookups?

______________________________________________________________________

# Summary

Most backend interview coding tasks revolve around transforming and organizing data rather than implementing complex
algorithms.

In this chapter, you learned:

- Filtering
- Mapping
- Finding
- Grouping
- Counting
- Sorting
- Flattening
- Removing duplicates
- Lookup tables
- Pagination
- Searching
- Deep copying
- Object transformations
- Async mapping
- Common collection patterns

These patterns appear frequently in real-world backend development and technical interviews. Mastering them will make
you significantly more productive when working with APIs, databases, and business logic.

______________________________________________________________________

# Next

[TypeScript Best Practices](14-best-practices.md)
