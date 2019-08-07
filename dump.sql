-- MySQL dump 10.13  Distrib 5.7.26, for osx10.14 (x86_64)
--
-- Host: localhost    Database: modakbul
-- ------------------------------------------------------
-- Server version	5.7.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `board` (
  `board_url` varchar(100) NOT NULL,
  `board_rank` int(11) DEFAULT NULL,
  `board_name` varchar(20) NOT NULL,
  `board_access` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`board_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
INSERT INTO `board` VALUES ('갤러리',3,'갤러리',1),('공지',0,'공지사항',1),('대외활동',5,'대외활동',1),('대외활동_공모전',0,'공모전',1),('대외활동_취업',1,'취업',1),('민원',4,'민원',0),('장부',2,'학생회비내역',1),('장부_데이터사이언스학과',1,'데이터사이언스학과',1),('장부_디자인이노베이션',3,'디자인이노베이션',1),('장부_만화애니메이션텍',2,'만화애니메이션텍',1),('장부_소프트웨어융합대학',4,'소프트웨어융합대학',1),('장부_소프트웨어학과',5,'소프트웨어학과',1),('장부_정보보호학과',6,'정보보호학과',1),('장부_지능기전공학부',7,'지능기전공학부',1),('장부_컴퓨터공학과',0,'컴퓨터공학과',1),('통계',7,'통계자료',1),('투표',6,'투표/설문조사',1),('학생회소개',1,'학생회소개',1);
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `dm_id` int(11) NOT NULL AUTO_INCREMENT,
  `dm_name` varchar(30) NOT NULL,
  `dm_chairman` varchar(50) NOT NULL,
  `dm_intro` varchar(5000) NOT NULL,
  `dm_img` varchar(500) NOT NULL,
  `dm_type` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`dm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'소프트웨어융합대학 학생회장','소융대 회장','안녕하세요.','baseprofileimg.png',0),(2,'소프트웨어융합대학 부학생회장','소융대 부회장','안녕하세요.','baseprofileimg.png',0),(3,'사무국','소융대 사무국장','안녕하세요.','baseprofileimg.png',1),(4,'기획국','소융대 기획국장','안녕하세요.','baseprofileimg.png',1),(5,'홍보국','소융대 홍보국장','안녕하세요.','baseprofileimg.png',1),(6,'민원국','소융대 민원국장','안녕하세요.','baseprofileimg.png',1);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `everyday_analysis`
--

DROP TABLE IF EXISTS `everyday_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `everyday_analysis` (
  `v_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `visitor_cnt` int(11) NOT NULL,
  `posts_cnt` int(11) NOT NULL,
  PRIMARY KEY (`v_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `everyday_analysis`
--

LOCK TABLES `everyday_analysis` WRITE;
/*!40000 ALTER TABLE `everyday_analysis` DISABLE KEYS */;
/*!40000 ALTER TABLE `everyday_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `log_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) DEFAULT NULL,
  `log_url` varchar(100) NOT NULL,
  `log_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19535 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (19532,'admin','/get_userinfo','2019-08-06 23:05:19'),(19533,'admin','/get_userinfo','2019-08-06 23:05:22'),(19534,'admin','/get_boards','2019-08-06 23:05:22');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) DEFAULT NULL,
  `post_title` varchar(100) NOT NULL,
  `post_content` mediumtext,
  `post_view` int(11) NOT NULL DEFAULT '0',
  `post_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `post_anony` tinyint(4) NOT NULL DEFAULT '0',
  `post_secret` tinyint(4) NOT NULL DEFAULT '0',
  `post_url_link` varchar(1000) DEFAULT NULL,
  `post_url_img` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1970 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_attach`
--

DROP TABLE IF EXISTS `post_attach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_attach` (
  `post_id` int(11) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  PRIMARY KEY (`post_id`,`file_path`),
  CONSTRAINT `post_attach_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_attach`
--

LOCK TABLES `post_attach` WRITE;
/*!40000 ALTER TABLE `post_attach` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_attach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_comment`
--

DROP TABLE IF EXISTS `post_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `comment` varchar(500) NOT NULL,
  `comment_anony` tinyint(4) NOT NULL DEFAULT '0',
  `comment_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment_parent` int(11) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  KEY `comment_parent` (`comment_parent`),
  CONSTRAINT `post_comment_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `post_comment_ibfk_3` FOREIGN KEY (`comment_parent`) REFERENCES `post_comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_comment`
--

LOCK TABLES `post_comment` WRITE;
/*!40000 ALTER TABLE `post_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_like`
--

DROP TABLE IF EXISTS `post_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_like` (
  `post_id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  PRIMARY KEY (`post_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_like_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_like_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_like`
--

LOCK TABLES `post_like` WRITE;
/*!40000 ALTER TABLE `post_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_tag`
--

DROP TABLE IF EXISTS `post_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_tag` (
  `post_id` int(11) NOT NULL,
  `tag_id` varchar(20) NOT NULL,
  PRIMARY KEY (`post_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `post_tag_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_tag`
--

LOCK TABLES `post_tag` WRITE;
/*!40000 ALTER TABLE `post_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `tag_id` varchar(20) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES ('ADMIN'),('갤러리'),('공모전'),('공지'),('대외활동'),('데이터사이언스학과'),('디자인이노베이션'),('디지털콘텐츠학과'),('만화애니메이션텍'),('민원'),('블랙리스트'),('소프트웨어융합대학'),('소프트웨어학과'),('외부사이트'),('장부'),('정보보호학과'),('지능기전공학부'),('창의소프트학부'),('취업'),('컴퓨터공학과'),('학생회소개');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `today_visitor`
--

DROP TABLE IF EXISTS `today_visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `today_visitor` (
  `ip_adress` varchar(20) NOT NULL,
  PRIMARY KEY (`ip_adress`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `today_visitor`
--

LOCK TABLES `today_visitor` WRITE;
/*!40000 ALTER TABLE `today_visitor` DISABLE KEYS */;
INSERT INTO `today_visitor` VALUES ('127.0.0.1');
/*!40000 ALTER TABLE `today_visitor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` varchar(20) NOT NULL,
  `pw` varchar(150) NOT NULL,
  `user_name` varchar(10) NOT NULL,
  `user_color` varchar(20) NOT NULL DEFAULT '#D8D8D8',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('16011040','pbkdf2:sha256:150000$Qi7NCyKF$4792f945692105732554db45ba2989f32a58e6726acaa59977a57af23b8041ca','임희원','#D8D8D8'),('16011075','pbkdf2:sha256:150000$bT034bMv$2f93a4a02085dd731d7ee12e1cb65069ace58f96ff780d8a3cb633410f95c529','김형석','#65d8cc'),('16011089','pbkdf2:sha256:150000$ibGY6gIA$bd819eb123ceae00c043a452372d573624d36bcdf56732aa85be72f86c85ea6e','신희재','#D8D8D8'),('16011092','pbkdf2:sha256:150000$bsYeTGaR$7489d804f35c4729bf8756f12c8be133f4168fa0c0e7b82e7bdecbf83ab24d6f','서정민','#2ed869'),('17011584','pbkdf2:sha256:150000$JuNwccIi$435ab0dd6147a467ebd09f20bea55c1def14f8b122809726ed14a6b25ecf5c92','정재경','#51a4d8'),('admin','pbkdf2:sha256:150000$BIqw0s98$8bda0cdcb70849c1a1cc95136c69988e117e11c91896ead1ac93d7e0006edc5e','관리자','#6f87d8'),('anony','익명용 유저입니다. 비밀번호는 없어요.','익명','#D8D8D8');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tag`
--

DROP TABLE IF EXISTS `user_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tag` (
  `user_id` varchar(20) NOT NULL,
  `tag_id` varchar(20) NOT NULL,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `user_tag_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tag`
--

LOCK TABLES `user_tag` WRITE;
/*!40000 ALTER TABLE `user_tag` DISABLE KEYS */;
INSERT INTO `user_tag` VALUES ('admin','ADMIN'),('16011040','블랙리스트'),('16011089','블랙리스트'),('17011584','블랙리스트'),('16011040','컴퓨터공학과'),('16011075','컴퓨터공학과'),('16011089','컴퓨터공학과'),('16011092','컴퓨터공학과'),('17011584','컴퓨터공학과');
/*!40000 ALTER TABLE `user_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `v_post`
--

DROP TABLE IF EXISTS `v_post`;
/*!50001 DROP VIEW IF EXISTS `v_post`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `v_post` AS SELECT 
 1 AS `post_id`,
 1 AS `user_id`,
 1 AS `post_title`,
 1 AS `post_content`,
 1 AS `post_view`,
 1 AS `post_date`,
 1 AS `post_anony`,
 1 AS `post_secret`,
 1 AS `post_url_link`,
 1 AS `post_url_img`,
 1 AS `user_name`,
 1 AS `user_color`,
 1 AS `comment_cnt`,
 1 AS `like_cnt`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `variable`
--

DROP TABLE IF EXISTS `variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variable` (
  `v_key` varchar(30) NOT NULL,
  `value` varchar(10000) NOT NULL,
  PRIMARY KEY (`v_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variable`
--

LOCK TABLES `variable` WRITE;
/*!40000 ALTER TABLE `variable` DISABLE KEYS */;
INSERT INTO `variable` VALUES ('연락처','02) 1588 - 1000<br /><br />학생회관 XXX 호'),('총인사말','안녕하세요.<br /><br />소프트웨어융합대학 번영 학생회 입니다.<br /><br />열심히 하겠습니다.'),('학생회로고','20190806205034724472_Modakbullogo_logo.png'),('학생회부제','Software Convergence University'),('학생회이름','BURN YOUNG');
/*!40000 ALTER TABLE `variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote` (
  `vote_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) DEFAULT NULL,
  `vote_title` varchar(100) NOT NULL,
  `vote_content` varchar(10000) NOT NULL,
  `start_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` datetime NOT NULL,
  `vote_file_path` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`vote_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_que`
--

DROP TABLE IF EXISTS `vote_que`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_que` (
  `que_id` int(11) NOT NULL AUTO_INCREMENT,
  `vote_id` int(11) NOT NULL,
  `que` varchar(100) NOT NULL,
  `que_type` tinyint(4) NOT NULL,
  PRIMARY KEY (`que_id`),
  KEY `vote_id` (`vote_id`),
  CONSTRAINT `vote_que_ibfk_1` FOREIGN KEY (`vote_id`) REFERENCES `vote` (`vote_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_que`
--

LOCK TABLES `vote_que` WRITE;
/*!40000 ALTER TABLE `vote_que` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_que` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_select`
--

DROP TABLE IF EXISTS `vote_select`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_select` (
  `select_id` int(11) NOT NULL AUTO_INCREMENT,
  `que_id` int(11) NOT NULL,
  `select_content` varchar(100) NOT NULL,
  PRIMARY KEY (`select_id`),
  KEY `que_id` (`que_id`),
  CONSTRAINT `vote_select_ibfk_1` FOREIGN KEY (`que_id`) REFERENCES `vote_que` (`que_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_select`
--

LOCK TABLES `vote_select` WRITE;
/*!40000 ALTER TABLE `vote_select` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_select` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_user_answer`
--

DROP TABLE IF EXISTS `vote_user_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_user_answer` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `vote_id` int(11) NOT NULL,
  `que_id` int(11) NOT NULL,
  `select_id` int(11) DEFAULT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `answer` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `vote_id` (`vote_id`),
  KEY `que_id` (`que_id`),
  KEY `select_id` (`select_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `vote_user_answer_ibfk_1` FOREIGN KEY (`vote_id`) REFERENCES `vote` (`vote_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_user_answer_ibfk_2` FOREIGN KEY (`que_id`) REFERENCES `vote_que` (`que_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_user_answer_ibfk_3` FOREIGN KEY (`select_id`) REFERENCES `vote_select` (`select_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_user_answer_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_user_answer`
--

LOCK TABLES `vote_user_answer` WRITE;
/*!40000 ALTER TABLE `vote_user_answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_user_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `v_post`
--

/*!50001 DROP VIEW IF EXISTS `v_post`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_post` AS (select `e`.`post_id` AS `post_id`,`e`.`user_id` AS `user_id`,`e`.`post_title` AS `post_title`,`e`.`post_content` AS `post_content`,`e`.`post_view` AS `post_view`,`e`.`post_date` AS `post_date`,`e`.`post_anony` AS `post_anony`,`e`.`post_secret` AS `post_secret`,`e`.`post_url_link` AS `post_url_link`,`e`.`post_url_img` AS `post_url_img`,`e`.`user_name` AS `user_name`,`e`.`user_color` AS `user_color`,`e`.`comment_cnt` AS `comment_cnt`,ifnull(`f`.`like_cnt`,0) AS `like_cnt` from (((select `c`.`post_id` AS `post_id`,`c`.`user_id` AS `user_id`,`c`.`post_title` AS `post_title`,`c`.`post_content` AS `post_content`,`c`.`post_view` AS `post_view`,`c`.`post_date` AS `post_date`,`c`.`post_anony` AS `post_anony`,`c`.`post_secret` AS `post_secret`,`c`.`post_url_link` AS `post_url_link`,`c`.`post_url_img` AS `post_url_img`,`c`.`user_name` AS `user_name`,`c`.`user_color` AS `user_color`,ifnull(`d`.`comment_cnt`,0) AS `comment_cnt` from (((select `A`.`post_id` AS `post_id`,if((`A`.`post_anony` = 0),`A`.`user_id`,'익명') AS `user_id`,`A`.`post_title` AS `post_title`,`A`.`post_content` AS `post_content`,`A`.`post_view` AS `post_view`,`A`.`post_date` AS `post_date`,`A`.`post_anony` AS `post_anony`,`A`.`post_secret` AS `post_secret`,`A`.`post_url_link` AS `post_url_link`,`A`.`post_url_img` AS `post_url_img`,if((`A`.`post_anony` = 0),`b`.`user_name`,'익명') AS `user_name`,if((`A`.`post_anony` = 0),`b`.`user_color`,'#D8D8D8') AS `user_color` from (`modakbul`.`post` `A` left join (select `modakbul`.`user`.`user_id` AS `user_id`,`modakbul`.`user`.`user_name` AS `user_name`,`modakbul`.`user`.`user_color` AS `user_color` from `modakbul`.`user`) `B` on((`A`.`user_id` = `b`.`user_id`))))) `C` left join (select `modakbul`.`post_comment`.`post_id` AS `post_id`,count(0) AS `comment_cnt` from `modakbul`.`post_comment` group by `modakbul`.`post_comment`.`post_id`) `D` on((`c`.`post_id` = `d`.`post_id`))))) `E` left join (select `modakbul`.`post_like`.`post_id` AS `post_id`,count(0) AS `like_cnt` from `modakbul`.`post_like` group by `modakbul`.`post_like`.`post_id`) `F` on((`e`.`post_id` = `f`.`post_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-06 23:26:18
