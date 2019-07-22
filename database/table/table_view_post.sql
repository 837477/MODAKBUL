CREATE OR REPLACE VIEW v_post AS (SELECT E.*, F.user_name FROM (SELECT D.*, ifnull(C.like_cnt, 0) AS like_cnt, ifnull(C.comment_cnt, 0) AS comment_cnt FROM (SELECT A.post_id, A.like_cnt, B.comment_cnt FROM (SELECT post_id, COUNT(*) AS like_cnt FROM post_like GROUP BY post_id) A LEFT JOIN (SELECT post_id, COUNT(*) AS comment_cnt FROM post_comment GROUP BY post_id) B ON A.post_id = B.post_id) C RIGHT JOIN (SELECT * FROM post) D ON C.post_id = D.post_id) E LEFT JOIN (SELECT user_id, user_name FROM user) F ON E.user_id = F.user_id);


/*
CREATE OR REPLACE VIEW V_post AS (SELECT F.*, ifnull(E.like_cnt,0) AS like_cnt, ifnull(E.comment_cnt, 0) AS comment_cnt, ifnull(E.attach_cnt,0) AS attach_cnt FROM (SELECT C.post_id, C.like_cnt, C.comment_cnt, D.attach_cnt FROM (SELECT A.post_id, A.like_cnt, B.comment_cnt FROM (SELECT post_id, COUNT(*) AS like_cnt FROM post_like GROUP BY post_id) A LEFT JOIN (SELECT post_id, COUNT(*) AS comment_cnt FROM post_comment GROUP BY post_id) B ON A.post_id = B.post_id) C LEFT JOIN (SELECT post_id, COUNT(*) AS attach_cnt FROM post_attach GROUP BY post_id) D ON C.post_id = D.post_id) E RIGHT JOIN (SELECT * FROM post) F ON E.post_id = F.post_id);
*/