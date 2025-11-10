/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT
	c.name
	,count(fc.film_id)
FROM
	category c
JOIN film_category fc ON
	fc.category_id = c.category_id
GROUP BY
	c."name"
ORDER BY
	2 DESC;
/*

2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT
	a.first_name || ' ' || a.last_name AS full_name
FROM
	actor a
JOIN film_actor fa ON
	fa.actor_id = a.actor_id
JOIN film f ON
	f.film_id = fa.film_id
JOIN inventory i ON
	i.film_id = f.film_id
JOIN rental r ON
	r.inventory_id = i.inventory_id
GROUP BY
	a.actor_id
ORDER BY
	count(*) DESC
LIMIT 10;
/*

3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT
	c.name AS category_name
	, SUM(p.amount) AS total_spent
FROM
	category c
JOIN film_category fc ON
	fc.category_id = c.category_id
JOIN inventory i ON
	i.film_id = fc.film_id
JOIN rental r ON
	r.inventory_id = i.inventory_id
JOIN payment p ON
	p.rental_id = r.rental_id
GROUP BY
	c.category_id,
	c.name
ORDER BY
	total_spent DESC,
	c.name
LIMIT 1;

-- more faster than previous
SELECT
	c.name
	, SUM(fm.amt) AS total_spent
FROM
	(
	SELECT
		i.film_id,
		SUM(p.amount) AS amt
	FROM
		payment p
	JOIN rental r ON
		r.rental_id = p.rental_id
	JOIN inventory i ON
		i.inventory_id = r.inventory_id
	GROUP BY
		i.film_id
) fm
JOIN film_category fc ON
	fc.film_id = fm.film_id
JOIN category c ON
	c.category_id = fc.category_id
GROUP BY
	c.category_id,
	c.name
ORDER BY
	total_spent DESC,
	c.name
LIMIT 1;
/*

4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT
	f.title
FROM
	film f
LEFT JOIN inventory i ON
	i.film_id = f.film_id
WHERE
	i.film_id IS NULL
ORDER BY
	f.film_id;
/*

5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
SELECT
	a.first_name || ' ' || a.last_name AS full_name
FROM
	actor a
JOIN film_actor fa ON
	fa.actor_id = a.actor_id
JOIN film f ON
	f.film_id = fa.film_id
JOIN film_category fc ON
	fc.film_id = f.film_id
JOIN category c ON
	c.category_id = fc.category_id
WHERE
	c."name" = 'Children'
GROUP BY
	a.actor_id
ORDER BY
	count(*) DESC, full_name
LIMIT 3;

WITH stats AS (
SELECT
	a.first_name || ' ' || a.last_name AS full_name, COUNT(*) AS cnt
FROM
	actor a
JOIN film_actor fa ON
	fa.actor_id = a.actor_id
JOIN film f ON
	f.film_id = fa.film_id
JOIN film_category fc ON
	fc.film_id = f.film_id
JOIN category c ON
	c.category_id = fc.category_id
WHERE
	c."name" = 'Children'
GROUP BY
	a.actor_id
)
SELECT full_name
FROM (
    SELECT full_name,
           ROW_NUMBER() OVER (ORDER BY cnt DESC, full_name) AS rn
    FROM stats
) t
WHERE rn <= 3;
