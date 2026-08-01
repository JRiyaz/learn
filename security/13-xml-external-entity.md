# Security - Part 13

# XML External Entity (XXE) - Overview

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What XXE is
- Why XXE happens
- Why modern backend applications are less affected
- Vulnerable Python examples
- Secure XML parsing
- Best practices

______________________________________________________________________

# What is XXE?

XXE stands for

**XML External Entity**.

It is a vulnerability that occurs when an application parses **untrusted XML** and allows the XML parser to load
external entities.

These external entities may allow an attacker to:

- Read local files
- Access internal services
- Cause Denial of Service (DoS)
- Leak sensitive information

______________________________________________________________________

# Why Does It Happen?

Some XML parsers support a feature called

```text id="xxe1301"
External Entities
```

These entities allow XML documents to reference external resources.

If the parser processes untrusted XML,

an attacker may abuse this feature.

______________________________________________________________________

# Typical Flow

```text id="xxe1302"
User Uploads XML

↓

Backend XML Parser

↓

External Entity Processed

↓

Sensitive Data Exposed
```

______________________________________________________________________

# Do We Still Need to Worry About XXE?

For most modern FastAPI applications,

the answer is:

**Not very often.**

Why?

Because modern backend APIs usually exchange data using:

```text id="xxe1303"
JSON
```

instead of

```text id="xxe1304"
XML
```

However,

many enterprise systems still use XML.

Examples include:

- SOAP Web Services
- Legacy enterprise applications
- Banking systems
- Government integrations
- Some document-processing systems

Understanding XXE is still useful for interviews and legacy projects.

______________________________________________________________________

# Real-World Example

Suppose your application accepts XML uploads.

Workflow

```text id="xxe1305"
User Uploads XML

↓

FastAPI

↓

XML Parser

↓

Extract Data
```

If the parser processes external entities,

the attacker may cause the parser to access resources it shouldn't.

______________________________________________________________________

# Vulnerable Python Example

Suppose the application parses XML like this.

```python id="xxe1306"
from lxml import etree

tree = etree.fromstring(
    xml_data
)
```

Depending on the parser configuration,

external entities may be processed.

The vulnerability is not in `lxml` itself,

but in how it is configured.

______________________________________________________________________

# The Root Problem

The issue isn't XML.

The issue is

parsing **untrusted XML**

using unsafe parser settings.

______________________________________________________________________

# Secure Solution

Configure the parser securely.

Example

```python id="xxe1307"
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
)

tree = etree.fromstring(
    xml_data,
    parser=parser,
)
```

Notice:

- External entities are disabled.
- Network access is disabled.

______________________________________________________________________

# Even Better

If your application doesn't require XML,

don't accept XML at all.

Prefer

```text id="xxe1308"
JSON
```

Modern REST APIs rarely need XML.

Reducing unnecessary features also reduces the attack surface.

______________________________________________________________________

# Secure Parsing Libraries

For Python,

consider secure libraries such as:

```text id="xxe1309"
defusedxml
```

`defusedxml` is specifically designed to protect against common XML attacks,

including XXE.

Example

```python id="xxe1310"
from defusedxml.ElementTree import fromstring

root = fromstring(xml_data)
```

______________________________________________________________________

# Defense in Depth

Secure XML processing combines:

```text id="xxe1311"
Accept JSON When Possible

↓

Disable External Entities

↓

Disable Network Access

↓

Use Secure XML Libraries

↓

Validate Input
```

______________________________________________________________________

# When Will You Encounter XXE?

You are most likely to encounter it when working with:

- SOAP APIs
- XML document uploads
- Legacy enterprise systems
- XML configuration files
- Third-party XML integrations

If your backend is entirely JSON-based,

XXE is much less likely.

______________________________________________________________________

# Best Practices

✅ Prefer JSON over XML.

✅ Disable external entities.

✅ Disable network access in XML parsers.

✅ Use secure XML libraries.

✅ Validate uploaded XML.

✅ Only enable XML support when necessary.

______________________________________________________________________

# Common Mistakes

### Accepting XML Without Need

If your API only requires JSON,

don't add XML support.

______________________________________________________________________

### Trusting Uploaded XML

Treat XML exactly like any other user input.

Never trust it.

______________________________________________________________________

### Using Default Parser Settings

Always review the security options

provided by your XML parser.

______________________________________________________________________

### Assuming Modern Frameworks Eliminate All Risk

Frameworks help,

but secure parser configuration

is still your responsibility.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| ------------------------- | -------------------------------------- |
| Default XML parser | Secure parser configuration |
| External entities enabled | External entities disabled |
| Network access allowed | Network access disabled |
| XML everywhere | JSON where possible |
| Untrusted parser | `defusedxml` or secure parser settings |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is XML External Entity (XXE), and how can developers prevent it?

XXE is a vulnerability that occurs when an application processes untrusted XML using a parser that allows external
entities. Attackers may exploit this to access local files, internal services, or other sensitive resources. Developers
can prevent XXE by disabling external entity resolution, disabling network access in XML parsers, using secure libraries
such as `defusedxml`, validating XML input, and preferring JSON instead of XML whenever possible.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What XXE is
- Why it happens
- Why modern APIs are less affected
- Secure XML parsing
- `defusedxml`
- Secure parser configuration
- Best practices

______________________________________________________________________

# What's Next

[Insecure Deserialization](14-insecure-deserialization.md)
