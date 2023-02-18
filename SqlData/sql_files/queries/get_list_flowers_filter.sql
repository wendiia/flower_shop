SELECT flavors.name, flowers.name, SUM(count)
FROM
    (SELECT id_flavor
    FROM orders
    WHERE date_begin BETWEEN ? and ?) query1
INNER JOIN flavors USING(id_flavor)
INNER JOIN composition USING (id_flavor)
INNER JOIN flowers USING (id_flower)
WHERE flowers.name =  ?
GROUP BY flavors.name