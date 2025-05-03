/*Part A*/
SELECT * FROM HumanResources.Employee;

/*1A*/
SELECT 
    BusinessEntityID, 
    PersonType, 
    FirstName, 
    LastName
FROM 
    Person.Person;

/*2A*/
SELECT DISTINCT 
    JobTitle
FROM 
    HumanResources.Employee
WHERE 
    JobTitle LIKE '%Manager%' 
    OR JobTitle LIKE '%Supervisor%' 
    OR JobTitle LIKE '%Chief%' 
    OR JobTitle LIKE '%Vice President%';

/*3A*/
SELECT 
    ProductID, 
    Name, 
    SellStartDate
FROM 
    Production.Product
WHERE 
    SellStartDate BETWEEN '2013-01-01' AND '2013-06-30'
ORDER BY 
    Name;

/*Part B*/
SELECT 
    p.FirstName || ' ' || p.LastName AS EmployeeName,
    e.JobTitle
FROM 
    HumanResources.Employee e
JOIN 
    Person.Person p ON e.BusinessEntityID = p.BusinessEntityID;

SELECT 
    p.FirstName || ' ' || p.LastName AS EmployeeName,
    e.JobTitle,
    ea.EmailAddress
FROM 
    HumanResources.Employee e
JOIN 
    Person.Person p ON e.BusinessEntityID = p.BusinessEntityID
JOIN 
    Person.EmailAddress ea ON p.BusinessEntityID = ea.BusinessEntityID;


/*Part C*/
/*1c*/
SELECT 
    Color,
    COUNT(*) AS NumberOfProducts
FROM 
    Production.Product
WHERE 
    Color IS NOT NULL AND Color <> ''
GROUP BY 
    Color
ORDER BY 
    NumberOfProducts DESC;

/*2c*/
SELECT 
    Color,
    CASE 
        WHEN p.FinishedGoodsFlag = TRUE THEN 'Finished Good'
        ELSE 'Not Finished Good'
    END AS ProductType,
    COUNT(*) AS NumberOfProducts
FROM 
    Production.Product p
WHERE 
    Color IS NOT NULL AND Color <> ''
GROUP BY 
    Color, ProductType
ORDER BY 
    NumberOfProducts DESC;

/*3c*/
SELECT 
    Color,
    CASE 
        WHEN p.FinishedGoodsFlag = TRUE THEN 'Finished Good'
        ELSE 'Not Finished Good'
    END AS ProductType,
    COUNT(*) AS NumberOfProducts
FROM 
    Production.Product p
WHERE 
    Color IS NOT NULL AND Color <> ''
GROUP BY 
    Color, ProductType
HAVING 
    COUNT(*) > 25
ORDER BY 
    NumberOfProducts DESC;

/*4c*/
SELECT 
    pc.Name AS ProductCategory,
    ROUND(SUM(soh.Freight), 2) AS TotalFreight
FROM 
    Sales.SalesOrderHeader soh
JOIN 
    Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
JOIN 
    Production.Product p ON sod.ProductID = p.ProductID
JOIN 
    Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
JOIN 
    Production.ProductCategory pc ON ps.ProductCategoryID = pc.ProductCategoryID
GROUP BY 
    pc.Name
ORDER BY 
    TotalFreight DESC;

/*Part D*/
SELECT 
    p.FirstName || ' ' || p.LastName AS EmployeeName,
    e.HireDate,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.HireDate)) AS YearsOfService,
    CASE 
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.HireDate)) >= 15 THEN 'Fully Vested'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.HireDate)) >= 10 THEN 'Partially Vested'
        ELSE 'Unvested'
    END AS VestingStatus
FROM 
    HumanResources.Employee e
JOIN 
    Person.Person p ON e.BusinessEntityID = p.BusinessEntityID;


