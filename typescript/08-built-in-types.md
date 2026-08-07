# Built-in Types & Collections

TypeScript inherits all of JavaScript's built-in data structures while adding static typing.

These collections are used constantly in backend development for:

- API responses
- Configuration
- Caching
- Request processing
- Data transformation
- Database results

Understanding them is essential for writing clean and efficient TypeScript code.

______________________________________________________________________

# Arrays

Arrays store ordered collections.

```typescript
const numbers: number[] = [

    10,

    20,

    30

];
```

______________________________________________________________________

Another syntax

```typescript
const numbers:

Array<number> = [

    10,

    20,

    30

];
```

Both are equivalent.

______________________________________________________________________

# Array Operations

Add

```typescript
numbers.push(40);
```

Remove last

```typescript
numbers.pop();
```

First element

```typescript
numbers.shift();
```

Add first

```typescript
numbers.unshift(5);
```

Length

```typescript
numbers.length;
```

______________________________________________________________________

# Iterating Arrays

Traditional

```typescript
for (

    const number

    of numbers

) {

    console.log(number);

}
```

______________________________________________________________________

forEach

```typescript
numbers.forEach(

    number =>

        console.log(number)

);
```

______________________________________________________________________

# map()

Transforms every element.

```typescript
const doubled =

numbers.map(

    number =>

        number * 2

);
```

Output

```typescript
[20,40,60]
```

______________________________________________________________________

# filter()

Keeps matching elements.

```typescript
const even =

numbers.filter(

    number =>

        number % 2 === 0

);
```

______________________________________________________________________

# find()

Returns first matching value.

```typescript
const value =

numbers.find(

    number =>

        number > 15

);
```

Output

```
20
```

______________________________________________________________________

# some()

Checks whether any element matches.

```typescript
const exists =

numbers.some(

    number =>

        number > 100

);
```

______________________________________________________________________

# every()

Checks whether every element matches.

```typescript
const valid =

numbers.every(

    number =>

        number > 0

);
```

______________________________________________________________________

# reduce()

One of the most important array methods.

Example

```typescript
const total =

numbers.reduce(

    (

        sum,

        number

    ) =>

        sum + number,

    0

);
```

Output

```
60
```

______________________________________________________________________

# sort()

```typescript
numbers.sort();
```

Problem

```
[10,2,30]
```

becomes

```
[10,2,30]
```

because strings are compared.

Correct

```typescript
numbers.sort(

    (a,b) =>

        a-b

);
```

Descending

```typescript
numbers.sort(

    (a,b) =>

        b-a

);
```

______________________________________________________________________

# Chaining

```typescript
const result =

numbers

.filter(

    number =>

        number > 10

)

.map(

    number =>

        number * 2

)

.sort(

    (a,b) =>

        a-b

);
```

Very common.

______________________________________________________________________

# Map

`Map` stores

```
Key

↓

Value
```

Unlike objects,

keys can be any type.

______________________________________________________________________

Creating Map

```typescript
const users =

new Map<

number,

string

>();
```

______________________________________________________________________

Add

```typescript
users.set(

    1,

    "Alice"

);
```

______________________________________________________________________

Get

```typescript
users.get(1);
```

______________________________________________________________________

Delete

```typescript
users.delete(1);
```

______________________________________________________________________

Check

```typescript
users.has(1);
```

______________________________________________________________________

Size

```typescript
users.size;
```

______________________________________________________________________

Loop

```typescript
for (

    const [

        key,

        value

    ]

    of users

) {

    console.log(

        key,

        value

    );

}
```

______________________________________________________________________

# Object vs Map

| Object | Map |
|---------|-----|
| String/Symbol keys | Any key type |
| Simpler syntax | More powerful |
| JSON friendly | Better for dynamic keys |
| Common for DTOs | Common for caches |

______________________________________________________________________

# Set

Stores

```
Unique values
```

Duplicates automatically disappear.

______________________________________________________________________

Create

```typescript
const skills =

new Set<string>();
```

______________________________________________________________________

Add

```typescript
skills.add("TypeScript");

skills.add("Node.js");

skills.add("TypeScript");
```

Result

```
TypeScript

Node.js
```

Only one copy.

______________________________________________________________________

Delete

```typescript
skills.delete(

    "Node.js"

);
```

______________________________________________________________________

Contains

```typescript
skills.has(

    "TypeScript"

);
```

______________________________________________________________________

Size

```typescript
skills.size;
```

______________________________________________________________________

Convert Set to Array

```typescript
const list =

[...skills];
```

Very common.

______________________________________________________________________

# Record

One of the most useful utility types.

Instead of

```typescript
{

    [key:string]:

    number

}
```

Use

```typescript
Record<

string,

number

>
```

______________________________________________________________________

Example

```typescript
const scores:

Record<

string,

number

> = {

    Alice: 90,

    Bob: 80

};
```

______________________________________________________________________

Backend Example

```typescript
type Users =

Record<

number,

string

>;
```

Equivalent

```
1

↓

Alice

2

↓

Bob
```

______________________________________________________________________

# Date

Create

```typescript
const now =

new Date();
```

Current year

```typescript
now.getFullYear();
```

Current month

```typescript
now.getMonth();
```

Current day

```typescript
now.getDate();
```

ISO String

```typescript
now.toISOString();
```

______________________________________________________________________

# JSON

Convert object

↓

JSON

```typescript
const json =

JSON.stringify(

    user

);
```

______________________________________________________________________

JSON

↓

Object

```typescript
const user =

JSON.parse(

    json

);
```

______________________________________________________________________

# Spread Operator

Copy array

```typescript
const copy =

[

...numbers

];
```

______________________________________________________________________

Merge arrays

```typescript
const all =

[

...a,

...b

];
```

______________________________________________________________________

Copy object

```typescript
const copy =

{

...user

};
```

______________________________________________________________________

Merge objects

```typescript
const employee =

{

...person,

...job

};
```

Very common in APIs.

______________________________________________________________________

# Rest Operator

Collect remaining values.

```typescript
function sum(

...numbers:

number[]

) {

}
```

Object

```typescript
const {

    id,

    ...details

} = user;
```

______________________________________________________________________

# Destructuring Arrays

```typescript
const [

    first,

    second

] = numbers;
```

______________________________________________________________________

# Destructuring Objects

```typescript
const {

    name,

    age

} = user;
```

Very common in Express controllers.

______________________________________________________________________

# Renaming

```typescript
const {

    name:

    username

} = user;
```

______________________________________________________________________

# Default Values

```typescript
const {

    city =

    "Unknown"

} = user;
```

______________________________________________________________________

# Optional Chaining

```typescript
user?.address?.city;
```

No runtime error if

```
address
```

doesn't exist.

______________________________________________________________________

# Nullish Coalescing

```typescript
const city =

user.city

??

"Unknown";
```

Unlike

```
||
```

this only replaces

```
null

undefined
```

______________________________________________________________________

# Object.keys()

Returns

```typescript
Object.keys(user);
```

Result

```typescript
["id","name"]
```

______________________________________________________________________

# Object.values()

```typescript
Object.values(user);
```

______________________________________________________________________

# Object.entries()

```typescript
Object.entries(user);
```

Result

```typescript
[

["id",1],

["name","Alice"]

]
```

______________________________________________________________________

# Object.assign()

Merge

```typescript
Object.assign(

    {},

    user,

    address

);
```

Modern code usually prefers

```typescript
{

...user,

...address

}
```

______________________________________________________________________

# Freeze Object

```typescript
Object.freeze(

    config

);
```

Makes the object immutable at runtime (shallow freeze).

______________________________________________________________________

# Backend Example

Transform database rows

```typescript
const users =

rows.map(

    row => ({

        id: row.id,

        name: row.name

    })

);
```

Very common in services.

______________________________________________________________________

# Grouping Data

```typescript
const grouped =

users.reduce(

(

    result,

    user

) => {

    result[

        user.role

    ] ??= [];

    result[

        user.role

    ].push(user);

    return result;

},

{} as Record<

string,

typeof users

>

);
```

Common interview pattern.

______________________________________________________________________

# Common Mistakes

## Using Object Instead of Map

If keys are dynamic or non-string,

use

```
Map
```

______________________________________________________________________

## Forgetting Numeric Sort

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

## Mutating Objects Accidentally

Instead of

```typescript
user.name = "Bob";
```

Sometimes prefer

```typescript
{

...user,

name:"Bob"

}
```

______________________________________________________________________

## Using ||

Wrong

```typescript
count || 0
```

Prefer

```typescript
count ?? 0
```

______________________________________________________________________

# Best Practices

✅ Prefer array methods (`map`, `filter`, `reduce`) for transformations.

✅ Use `Map` for dynamic key/value collections.

✅ Use `Set` for uniqueness.

✅ Use `Record` for typed dictionaries.

✅ Prefer spread syntax over `Object.assign()`.

✅ Use destructuring to simplify code.

✅ Prefer `??` over `||` for default values.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between an Object and a Map?

### Answer

Objects are primarily designed for structured data with string or symbol keys and are commonly used for JSON and DTOs.

`Map` supports keys of any type, preserves insertion order, provides convenient methods such as `set()` and `get()`, and
is generally preferred for dynamic key/value collections.

______________________________________________________________________

## Question

When should you use a Set?

### Answer

A `Set` should be used when you need to store unique values and automatically eliminate duplicates. It is commonly used
for tags, permissions, IDs, and deduplication tasks.

______________________________________________________________________

## Question

What is `Record<K, V>`?

### Answer

`Record<K, V>` is a utility type that creates an object type where each key of type `K` maps to a value of type `V`. It
is commonly used for dictionaries and lookup tables.

______________________________________________________________________

## Question

Why is the spread operator widely used?

### Answer

The spread operator provides a concise way to copy and merge arrays or objects while supporting immutable update
patterns, which improves readability and reduces accidental mutations.

______________________________________________________________________

## Question

Why should `??` usually be preferred over `||`?

### Answer

`||` treats values such as `0`, `false`, and empty strings as falsy, potentially replacing valid values.

`??` only falls back when the value is `null` or `undefined`, making it safer for backend applications.

______________________________________________________________________

# Practice Questions

1. What is the difference between `map()` and `filter()`?
1. What does `reduce()` do?
1. When should you use a `Map` instead of an object?
1. When should you use a `Set`?
1. What is `Record<K, V>`?
1. What is the spread operator used for?
1. What is object destructuring?
1. What is the difference between `??` and `||`?
1. What does `Object.entries()` return?
1. Why is immutable object copying considered a good practice?

______________________________________________________________________

# Summary

TypeScript's built-in collections and utility features make it easy to work with structured backend data.

In this chapter, you learned:

- Arrays
- Array methods (`map`, `filter`, `find`, `reduce`, `sort`)
- `Map`
- `Set`
- `Record`
- `Date`
- `JSON`
- Spread operator
- Rest operator
- Destructuring
- Optional chaining
- Nullish coalescing
- `Object.keys()`, `values()`, and `entries()`
- Immutable update patterns

These tools are used daily when processing API requests, database results, configuration, and business logic. The next
chapter introduces **Advanced TypeScript Features**, including utility types such as `Partial`, `Pick`, `Omit`, and
`Readonly`, which are heavily used in modern TypeScript frameworks.

______________________________________________________________________

# Next

[Advanced TypeScript Features](09-advanced-typescript.md)
