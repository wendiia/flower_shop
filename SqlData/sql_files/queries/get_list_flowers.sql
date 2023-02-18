SELECT flowers.name, SUM(count)
FROM
    (SELECT id_flavor
    FROM orders
    WHERE date_begin BETWEEN ? and ?) query1
INNER JOIN composition USING (id_flavor)
INNER JOIN flowers USING (id_flower)
GROUP BY flowers.name
