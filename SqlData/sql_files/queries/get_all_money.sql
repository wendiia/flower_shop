SELECT SUM(cost)
FROM orders
INNER JOIN flavors USING(id_flavor)

