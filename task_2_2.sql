SELECT 
    r.barcode, 
    r.price,
    p.title
FROM 
    reports r
JOIN 
    pos p ON r.pos_id = p.id
WHERE 
    p.title IN (
        SELECT 
            title
        FROM 
            pos
        GROUP BY 
            title
        HAVING 
            COUNT(*) > 1
    );