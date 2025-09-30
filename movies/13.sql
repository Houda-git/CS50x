SELECT DISTINCT p2.name FROM people p1 JOIN stars s1 ON s1.person_id = p1.id
JOIN stars s2 ON s2.movie_id = s1.movie_id
JOIN people p2 ON p2.id = s2.person_id
WHERE p1.name = 'Kevin Bacon' AND p1.birth = '1958'
AND p2.name != 'Kevin Bacon';
