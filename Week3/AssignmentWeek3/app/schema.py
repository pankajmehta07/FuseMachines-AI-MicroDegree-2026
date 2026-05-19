SCHEMA = """
DATABASE: classicmodels (PostgreSQL)

CRITICAL RULE: This database was created with quoted identifiers.
ALL mixed-case column names MUST be wrapped in double quotes in every query.
Example: c."customerNumber" NOT c.customerNumber

TABLE: customers
  - "customerNumber"            INT       (Primary Key)
  - "customerName"              VARCHAR
  - "contactLastName"           VARCHAR
  - "contactFirstName"          VARCHAR
  - phone                       VARCHAR
  - "addressLine1"              VARCHAR
  - "addressLine2"              VARCHAR
  - city                        VARCHAR
  - state                       VARCHAR
  - "postalCode"                VARCHAR
  - country                     VARCHAR
  - "salesRepEmployeeNumber"    INT       (Foreign Key → employees."employeeNumber")
  - "creditLimit"               DECIMAL

TABLE: orders
  - "orderNumber"               INT       (Primary Key)
  - "orderDate"                 DATE
  - "requiredDate"              DATE
  - "shippedDate"               DATE
  - status                      VARCHAR
  - comments                    TEXT
  - "customerNumber"            INT       (Foreign Key → customers."customerNumber")

TABLE: orderdetails
  - "orderNumber"               INT       (FK → orders."orderNumber")
  - "productCode"               VARCHAR   (FK → products."productCode")
  - "quantityOrdered"           INT
  - "priceEach"                 DECIMAL
  - "orderLineNumber"           INT

TABLE: products
  - "productCode"               VARCHAR   (Primary Key)
  - "productName"               VARCHAR
  - "productLine"               VARCHAR   (FK → productlines."productLine")
  - "productScale"              VARCHAR
  - "productVendor"             VARCHAR
  - "productDescription"        TEXT
  - "quantityInStock"           INT
  - "buyPrice"                  DECIMAL
  - "MSRP"                      DECIMAL

TABLE: productlines
  - "productLine"               VARCHAR   (Primary Key)
  - "textDescription"           TEXT
  - "htmlDescription"           TEXT

TABLE: employees
  - "employeeNumber"            INT       (Primary Key)
  - "lastName"                  VARCHAR
  - "firstName"                 VARCHAR
  - extension                   VARCHAR
  - email                       VARCHAR
  - "officeCode"                VARCHAR   (FK → offices."officeCode")
  - "reportsTo"                 INT       (FK → employees."employeeNumber")
  - "jobTitle"                  VARCHAR

TABLE: offices
  - "officeCode"                VARCHAR   (Primary Key)
  - city                        VARCHAR
  - phone                       VARCHAR
  - "addressLine1"              VARCHAR
  - "addressLine2"              VARCHAR
  - state                       VARCHAR
  - country                     VARCHAR
  - "postalCode"                VARCHAR
  - territory                   VARCHAR

TABLE: payments
  - "customerNumber"            INT       (Primary Key + FK → customers."customerNumber")
  - "checkNumber"               VARCHAR   (Primary Key)
  - "paymentDate"               DATE
  - amount                      DECIMAL

RELATIONSHIPS:
  - customers."salesRepEmployeeNumber" → employees."employeeNumber"
  - orders."customerNumber"            → customers."customerNumber"
  - orderdetails."orderNumber"         → orders."orderNumber"
  - orderdetails."productCode"         → products."productCode"
  - products."productLine"             → productlines."productLine"
  - employees."officeCode"             → offices."officeCode"
  - employees."reportsTo"              → employees."employeeNumber"
  - payments."customerNumber"          → customers."customerNumber"
"""