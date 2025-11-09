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
WITH top_film AS (
SELECT
	f.film_id
FROM
	film f
JOIN inventory i ON
	i.film_id = f.film_id
JOIN rental r ON
	r.inventory_id = i.inventory_id
GROUP BY
	f.film_id
ORDER BY
	COUNT(*) * f.rental_rate DESC
LIMIT 1
)
SELECT
	c.name
FROM
	category c
JOIN film_category fc ON
	fc.category_id = c.category_id
JOIN top_film tf ON
	tf.film_id = fc.film_id;
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
