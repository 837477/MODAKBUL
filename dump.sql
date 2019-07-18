-- MySQL dump 10.13  Distrib 5.7.26, for osx10.14 (x86_64)
--
-- Host: localhost    Database: modakbul
-- ------------------------------------------------------
-- Server version	5.7.26

-- sudo mysqldump modakbul > dump.sql -u root -p
-- mysql -u root -p modakbul < dump.sql

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) DEFAULT NULL,
  `account_title` varchar(100) NOT NULL,
  `account_content` varchar(10000) NOT NULL,
  `account_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `account_budget` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`account_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_attach`
--

DROP TABLE IF EXISTS `account_attach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_attach` (
  `account_id` int(11) NOT NULL,
  `account_file_path` varchar(500) NOT NULL,
  PRIMARY KEY (`account_id`,`account_file_path`),
  CONSTRAINT `account_attach_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_attach`
--

LOCK TABLES `account_attach` WRITE;
/*!40000 ALTER TABLE `account_attach` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_attach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_form`
--

DROP TABLE IF EXISTS `account_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_form` (
  `form_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `form` varchar(100) NOT NULL,
  `trader` varchar(100) NOT NULL,
  `item` varchar(100) NOT NULL,
  `price` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`form_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `account_form_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_form`
--

LOCK TABLES `account_form` WRITE;
/*!40000 ALTER TABLE `account_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_tag`
--

DROP TABLE IF EXISTS `account_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_tag` (
  `account_id` int(11) NOT NULL,
  `tag_id` varchar(20) NOT NULL,
  PRIMARY KEY (`account_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `account_tag_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `account_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_tag`
--

LOCK TABLES `account_tag` WRITE;
/*!40000 ALTER TABLE `account_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_tag` ENABLE KEYS */;
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
  `post_content` varchar(10000) NOT NULL,
  `post_view` int(11) NOT NULL DEFAULT '0',
  `post_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `post_anony` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,'ADMIN','소프트웨어융합대학 동아리 활동보고서 양식','5월 20일부터 한달동안 동아리에서 진행한 활동 내용을 정리하여 sejongsc3@gmail.com 으로 보내주세요~.\n활동보고서는 한달 간격으로 보내주시면 됩니다!',0,'2019-07-17 21:01:28',0),(2,'ADMIN','소프트웨어융합대학 동아리 신청 안내 및 양식','※젊음을, 불태워라!※ ;\n \n안녕하세요! 제 3대 소프트웨어융합대학 번영 [BURN;YOUNG] 학생회입니다.\n저희 번영에서 소융대인의 활발한 동아리 활동을 지원하기 위하여 2019학년도 소융대 동아리 모집을 시작하였습니다.\n정식 동아리로 승격 될 경우 더 많은 교류 및 홍보를 할 수 있는 기회와 소정의 지원금이 지급됩니다.\n \n지원 방법\n1. \'신청양식\' 다운로드\n2. 신청서 작성 후 메일로 제출!\n➡ sejongsc3@gmail.com\n \n지원 기간\n5월 1일 (월) - 5월 10일 (금)\n \n제출 서류\n1. 동아리 등록서류\n2. 동아리 등록_동아리활동계획서\n \n \n반드시 동아리 신청 전에 동아리 등록회칙을 읽어주시길 바랍니다.\n동아리 등록회칙을 읽지 않아 발생하는 불이익은 신청자 본인에게 책임이 있습니다.',0,'2019-07-17 21:03:00',0),(3,'ADMIN','세종소융봉사 멘티 신청 안내 및 양식','안녕하세요! 제 3대 소프트웨어융합대학 번영 [BURN;YOUNG] 학생회입니다.\n저희 번영에서 소융대 학생이면 누구나 참여할 수 있는 멘토멘티 프로그램인 \'세.소.봉\'을 진행하려고 합니다.\n \n\'세.소.봉\'이란 \'세종 소융 봉사\'의 줄임말로 멘토에겐 자신의 전공을 살릴 수 있는 뜻 깊은 멘토링 기회와 세사봉 인증 봉사시간을 제공하며\n멘티에겐 학점에 구애받지 않고 배우고 싶었던 수업을 무료로 접할 수 있는 기회를 주는 프로그램입니다.',0,'2019-07-17 21:06:02',0),(4,'ADMIN','제3대 소프트웨어융합대학 번영 학생회 수습지원서 양식','제출기간 : 2019.04.03 자정까지',0,'2019-07-17 21:06:52',0),(5,'ADMIN','제4회 소프트웨어융합대학 후보자 등록 구비서류','(참고) 2019 소프트웨어융합대학 선거 일정\n3/5 발족공고\n3/6 ~ 3/8 1차사퇴\n3/6 ~ 3/15 후보자추천\n3/11 ~ 3/15 후보자등록\n3/13 2차선거후보자 및 선거운동원 사퇴\n3/15 후보자심사\n3/18 ~ 3/22 선거운동\n3/20 공청회\n3/25 ~ 3/28 투표운동\n3/28 개표 및 개표결과 공고\n3/29 당선공고',0,'2019-07-17 21:07:17',0),(6,'ADMIN','세종대학교 소프트웨어융합대학 학생회 회칙 및 재정운용 세칙(2018년도 개정)','세종대학교 소프트웨어융합대학 학생회 회칙 및 재정운용 세칙(2018년도 개정)',0,'2019-07-17 21:08:04',0),(7,'ADMIN','소프트웨어융합대학 학생회 회칙 개정안','전체학생대표자대회 결과 공고\n \n안녕하십니까. 제2대 소프트웨어융합대학 학생회입니다. 지난 11월 선거 무산과 함께 제3대 소프트웨어융합대학 선거관리위원회는 학우여러분의 시험기간 및 종강을 고려하여 재선거를 3월에 실시하기로 하였습니다.',0,'2019-07-17 21:09:30',0),(8,'ADMIN',' 제3대 소프트웨어융합대학 학생회 선거 후보자 공청회 신문','2018년 11월 16일에 진행된 제3대 소프트웨어융합대학 학생회 선거 후보자 공청회 내용 정리본입니다.\n신문 발행에 어려움이 있어, 온라인 배포로 대신합니다.\n \n제3대 소프트웨어융합대학 학생회 선거 단일후보 \'소다\' 선거운동본부의 자세한 공약이 궁금하시다면,\n공지사항에 업로드 되어있는 공약집을 확인하시면 됩니다.\n \n11월 26일 (월)부터 11월 29일(목)까지 투표가 진행되니,\n소융대 학우분들의 많은 관심과 참여 부탁드립니다.',0,'2019-07-17 21:10:01',0),(9,'ADMIN','제3대 소프트웨어융합대학 학생회 단일후보 \'소다\' 선거운동본부 정책자료집','안녕하십니까 제3대 소프트웨어융합대학 선거관리위원회입니다.\n \n제3대 소프트웨어융합대학 학생회 단일후보 \'소다\' 선거운동본부 정책자료집 업로드합니다.\n자유롭게 열람하신 뒤,\n선거  투표 기간(11월 26일 ~ 11월 29일)에 소융인 여러분의 소중한 한 표 부탁드립니다.',0,'2019-07-17 21:10:26',0),(10,'ADMIN','소프트웨어융합대학 선거 시행 세칙, 회칙','소프트웨어융합대학 선거 시행 세칙, 학생회 회칙입니다.',0,'2019-07-17 21:10:50',0),(11,'ADMIN','제3회 소프트웨어융합대학 후보자 등록 구비서류','제3회 소프트웨어융합대학 후보자 등록 구비서류입니다.\n \n(참고) 2019 소프트웨어융합대학 선거 일정 \n- 10월 29일 (화) : 소융대 선거관리위원회 발족\n- 10월 31일 (수) ~ 11월 4일 (일) : 선거 후보자 및 선거운동원 사퇴 기간\n- 11월 5일 (월) ~ 11월 9일 (금) : 선거 후보자 추천 및 1차 선거 운동원 등록 기간\n- 11월 9일 (금) : 선거 후보자 심사\n- 11월 12일 (월) ~ 11월 23일 (금) : 선거운동 기간\n- 11월 15일 (목) : 2차 선거운동원 사퇴 및 등록\n- 11월 15일 (목) : 선거 후보자 공청회\n- 11월 26일 (월) ~ 11월 29일 (목) : 투표 기간\n- 11월 29일 (목) : 개표',0,'2019-07-17 21:11:12',0),(12,'ADMIN','Importance Of Parenting And Gift Ideas For Parents\' Day','Each year the fourth Sunday of July honours parents for their hard work they put into nurturing the family without any complaints. President Bill Clinton founded Parents\' Day in 1994 when he signed a Congressional Resolution into law. This day acknowledges, uplifts, and supports the importance of parents in the bringing up of children.\n\nThere are separate days commemorated to each parent and each of these special occasions is an ideal gift giving opportunity. However, a day, which appreciates both the parents together, calls for presents, which mum and dad can share together. Here are some suggestions:\n\nGift Certificates: Parents struggle too hard to provide an ease of life for the kids. A gift voucher would allow them to buy things, which would give them all the comfort they need.\n\nRecipe Books: If both the parents share their love for cooking and like to experiment with food and ingredients, gift them a big, fat recipe book that includes popular cuisines from all around the world.\n\nDigital Picture Frames: Pre-upload pictures in a digital photo frame, of the best moments you spent with your parents and let them relive moments repeatedly.\n\nPersonalized Gifts: Nothing expresses true gratitude and affection like personalized gifts. Starting from mugs to almost anything, choose wisely to personalize a lovely gift and make Parents\' Day memorable.',0,'2019-07-17 21:25:11',0),(13,'ADMIN','2019 소융대 공모전 1차 기획서 양식','1차 기획안 제출 기간6월 9일부터 7월 7일 23시 59분까지. 기획안으로 보내주시면 감사하겠습니다. 자세한 문의사으로 문의 부탁드립니다.감사합니다.',0,'2019-07-17 21:28:00',0),(14,'ADMIN','2019년도 소융대 공모전 안내','젊음을 불태워라!',0,'2019-07-17 21:28:48',0);
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
  `comment_anony` tinyint(4) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_comment_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
INSERT INTO `post_tag` VALUES (13,'공모전'),(14,'공모전'),(1,'공지'),(2,'공지'),(3,'공지'),(4,'공지'),(5,'공지'),(6,'공지'),(7,'공지'),(8,'공지'),(9,'공지'),(10,'공지'),(11,'공지'),(13,'소프트웨어융합대학'),(14,'소프트웨어융합대학');
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
INSERT INTO `tag` VALUES ('ADMIN'),('갤러리'),('공모전'),('공지'),('데이터사이언스학과'),('디자인이노베이션'),('만화애니메이션텍'),('민원'),('소프트웨어융합대학'),('소프트웨어학과'),('장부'),('정보보호학과'),('지능기전공학부'),('컴퓨터공학과');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
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
  `introduce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('16011075','123','김형석','D8D8D8','안녕하세요 대구미남 입니다.'),('16011089','123','신희재','D8D8D8','안녕하세요 부산미남 입니다.'),('16011092','123','서정민','D8D8D8','안녕하세요 광주미남 입니다.'),('17011584','123','정재경','D8D8D8','안녕하세요 서울미남 입니다.'),('ADMIN','123','관리자','D8D8D8','안녕하세요 모닥불 관리자 입니다.');
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
INSERT INTO `user_tag` VALUES ('ADMIN','ADMIN'),('17011584','데이터사이언스학과'),('16011089','정보보호학과'),('16011075','지능기전공학부'),('16011092','컴퓨터공학과');
/*!40000 ALTER TABLE `user_tag` ENABLE KEYS */;
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
  PRIMARY KEY (`vote_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_attach`
--

DROP TABLE IF EXISTS `vote_attach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_attach` (
  `vote_id` int(11) NOT NULL,
  `vote_file_path` varchar(500) NOT NULL,
  PRIMARY KEY (`vote_id`,`vote_file_path`),
  CONSTRAINT `vote_attach_ibfk_1` FOREIGN KEY (`vote_id`) REFERENCES `vote` (`vote_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_attach`
--

LOCK TABLES `vote_attach` WRITE;
/*!40000 ALTER TABLE `vote_attach` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_attach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_content_type`
--

DROP TABLE IF EXISTS `vote_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_content_type` (
  `content_type_id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `content_type_title` varchar(10) NOT NULL,
  PRIMARY KEY (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_content_type`
--

LOCK TABLES `vote_content_type` WRITE;
/*!40000 ALTER TABLE `vote_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_que`
--

DROP TABLE IF EXISTS `vote_que`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_que` (
  `vote_que_id` int(11) NOT NULL AUTO_INCREMENT,
  `vote_id` int(11) NOT NULL,
  `que_title` varchar(100) NOT NULL,
  `content_type_id` tinyint(4) NOT NULL,
  PRIMARY KEY (`vote_que_id`),
  KEY `vote_id` (`vote_id`),
  KEY `content_type_id` (`content_type_id`),
  CONSTRAINT `vote_que_ibfk_1` FOREIGN KEY (`vote_id`) REFERENCES `vote` (`vote_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_que_ibfk_2` FOREIGN KEY (`content_type_id`) REFERENCES `vote_content_type` (`content_type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
  `select_content` varchar(100) NOT NULL,
  `vote_que_id` int(11) NOT NULL,
  PRIMARY KEY (`select_id`),
  KEY `vote_que_id` (`vote_que_id`),
  CONSTRAINT `vote_select_ibfk_1` FOREIGN KEY (`vote_que_id`) REFERENCES `vote_que` (`vote_que_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_select`
--

LOCK TABLES `vote_select` WRITE;
/*!40000 ALTER TABLE `vote_select` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_select` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_tag`
--

DROP TABLE IF EXISTS `vote_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_tag` (
  `vote_id` int(11) NOT NULL,
  `tag_id` varchar(20) NOT NULL,
  PRIMARY KEY (`vote_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `vote_tag_ibfk_1` FOREIGN KEY (`vote_id`) REFERENCES `vote` (`vote_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_tag`
--

LOCK TABLES `vote_tag` WRITE;
/*!40000 ALTER TABLE `vote_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_tag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-17 21:39:36
