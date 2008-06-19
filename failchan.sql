-- MySQL dump 10.9
--
-- Host: localhost    Database: failchan
-- ------------------------------------------------------
-- Server version	4.1.22-standard

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `extlist`
--

DROP TABLE IF EXISTS `extlist`;
CREATE TABLE `extlist` (
  `id` int(11) NOT NULL auto_increment,
  `path` varchar(255) NOT NULL default '',
  `thwidth` int(11) NOT NULL default '0',
  `thheight` int(11) NOT NULL default '0',
  `ext` varchar(16) NOT NULL default '',
  `type` varchar(16) NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `extlist`
--

LOCK TABLES `extlist` WRITE;
/*!40000 ALTER TABLE `extlist` DISABLE KEYS */;
INSERT INTO `extlist` VALUES (1,'',0,0,'jpg','image'),(2,'',0,0,'jpeg','image'),(3,'',0,0,'gif','image'),(4,'',0,0,'bmp','image'),(5,'',0,0,'png','image'),(6,'',0,0,'pcx','image'),(7,'',0,0,'tiff','image'),(8,'',0,0,'ico','image-jpg'),(9,'',0,0,'tga','image-jpg'),(10,'',0,0,'psd','image-jpg'),(11,'../generic/archive.png',128,128,'rar','archive'),(12,'../generic/archive.png',128,128,'tgz','archive'),(13,'../generic/archive.png',128,128,'tbz','archive'),(14,'../generic/archive.png',128,128,'gz','archive'),(15,'../generic/archive.png',128,128,'zip','archive'),(16,'../generic/archive.png',128,128,'torrent','torrent'),(17,'../generic/sound.png',128,128,'mp3','music'),(18,'../generic/sound.png',128,128,'midi','music'),(19,'../generic/sound.png',128,128,'wav','music'),(20,'../generic/text.png',128,128,'txt','text'),(21,'../generic/text.png',128,128,'log','text'),(22,'../generic/text.png',128,128,'rtf','text'),(23,'../generic/text.png',128,128,'php','source'),(24,'../generic/text.png',128,128,'py','source'),(25,'../generic/text.png',128,128,'mako','source'),(26,'../generic/text.png',128,128,'sql','data'),(27,'../generic/text.png',128,128,'pl','source'),(28,'../generic/pdf.png',128,128,'pdf','source');
/*!40000 ALTER TABLE `extlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invites`
--

DROP TABLE IF EXISTS `invites`;
CREATE TABLE `invites` (
  `id` int(11) NOT NULL auto_increment,
  `invite` varchar(128) NOT NULL default '',
  `date` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `invites`
--

LOCK TABLES `invites` WRITE;
/*!40000 ALTER TABLE `invites` DISABLE KEYS */;
INSERT INTO `invites` VALUES (5,'0953164facff3a51619fee00164e0e02b0bb23075d22e7ce5ffa7ec0fdc9c08be2b3d23278ee65a0fb992b84ba8a80e4c2deeddc09a383b2a268291fd2d8c155','2008-06-13 04:09:43'),(6,'b717e0dd11f1c8c1f16c70719e300fb86f38c43c4d01d2d3dc861147721db134f2b9534d208c25e7823e3a7620638e5ce41d18d8afabca0b66c94fffaf875bf5','2008-06-13 04:09:43'),(7,'f36895082c1c890d543025e6ff5ebf1379ac64067b768e9dcc1a6ce8d4e7a5697658b8bda1d4a6d0d5dc7089dcc37ce0e2e64893827c1386dd4f70d9b8cfdb91','2008-06-13 04:09:46'),(11,'893e5df202c20c1a1755a150db90f9f5ca700cc1470a4d92cf38399eaba54a31248102736bbfc3e27fc6acb7665384a75a3bd6336c0832a271ac9b259656670c','2008-06-13 04:09:54'),(9,'fc100376f0883d1b807a10a49fc72df1b498ed389e87f332fb9c33ff7a340af4a2ed22308338615663ef709f01c30127fb20a2826f4f889312768f9630bbfcaa','2008-06-13 04:09:49'),(10,'36f55871478c36a648380444ac5e2a83a63a49c8f1b171c86d920a9436d80b06217add67c444a516f2cfca9a40bed689655b6e673cd376cd2d553b7f0f33ba10','2008-06-13 04:09:51'),(21,'81d54ab3700e5b357dbca6135d5f0f9e7aadfce1c500b541b491b0dcb077c67b5576675bf98d2cb8ae97b2b0f678a0f46849243b8860fe6967cc030de658f8bc','2008-06-15 08:12:33'),(23,'c0ce58d6dd69b4c2370a589d890c4e228b656131740a8e8505e4acf4e702df4ead54f79ff33407d09700924fb15ae5793b92af8fd9f2603845336420b78124f8','2008-06-15 08:30:04'),(26,'4cced7f3dc022393b78b55868367bb381a8ed409300dca4da2a3a1e51cdb368c04250b7f87a8f36211e66160e0cd4763274ea0e8247d5260b77b25b7855c3bf8','2008-06-18 14:02:14');
/*!40000 ALTER TABLE `invites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oekaki`
--

DROP TABLE IF EXISTS `oekaki`;
CREATE TABLE `oekaki` (
  `id` int(11) NOT NULL auto_increment,
  `tempid` bigint(20) default NULL,
  `picid` int(11) NOT NULL default '0',
  `time` int(11) NOT NULL default '0',
  `source` int(11) NOT NULL default '0',
  `uid_number` int(11) NOT NULL default '0',
  `type` varchar(255) NOT NULL default '',
  `path` varchar(255) NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `oekaki`
--

LOCK TABLES `oekaki` WRITE;
/*!40000 ALTER TABLE `oekaki` DISABLE KEYS */;
INSERT INTO `oekaki` VALUES (1,2147483647,-1,-1,14,13,'Shi normal',''),(2,2147483647,-1,-1,14,6,'Shi normal',''),(3,12136315023764948,-1,-1,14,13,'Shi normal',''),(4,12136315970968080,-1,34891,29,13,'Shi normal','12136315970968080.png'),(5,12136339876362260,-1,-1,63,13,'Shi normal',''),(6,12136345464670110,-1,59640,0,13,'Shi normal','12136345464670110.png'),(7,12136351792312232,-1,-1,21,13,'Shi normal',''),(8,12136358255518438,-1,-1,65,13,'Shi normal',''),(9,12136358911864050,-1,-1,64,6,'Shi normal',''),(10,12136359151552710,-1,25031,64,6,'Shi normal','12136359151552710.png'),(11,12136550978219430,-1,-1,66,13,'Shi normal',''),(12,12136803371597190,-1,10391,64,9,'Shi normal','12136803371597190.png'),(13,12136806510728090,-1,23500,70,9,'Shi normal','12136806510728090.png'),(14,12136973542860860,-1,128391,65,9,'Shi normal','12136973542860860.png'),(15,12137238148957738,-1,-1,71,12,'Shi normal',''),(16,12137239009853972,-1,-1,68,12,'Shi normal',''),(17,12137252622795790,-1,-1,70,14,'Shi normal',''),(18,12137261839704890,-1,-1,79,14,'Shi normal',''),(19,12137276831510570,-1,203469,0,8,'Shi normal','12137276831510570.png'),(20,12137279718192250,-1,-1,60,8,'Shi normal',''),(21,12137950576449760,-1,-1,79,9,'Shi normal',''),(22,12138282718890550,-1,-1,29,6,'Shi normal',''),(23,12138836398618130,-1,-1,79,9,'Shi normal',''),(24,12138886152555420,-1,-1,21,6,'Shi normal',''),(25,12138891489690620,-1,-1,101,13,'Shi normal',''),(26,12138891545270200,-1,180813,101,13,'Shi normal','12138891545270200.png'),(27,12138902065801940,-1,178000,29,15,'Shi normal','12138902065801940.png'),(28,12138907245096418,-1,-1,68,9,'Shi normal',''),(29,12138926589452700,-1,-1,29,15,'Shi normal',''),(30,12138927866353460,-1,-1,110,15,'Shi normal',''),(31,12138928454283832,-1,-1,64,15,'Shi normal',''),(32,12138929127681350,-1,-1,0,15,'Shi normal','');
/*!40000 ALTER TABLE `oekaki` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `piclist`
--

DROP TABLE IF EXISTS `piclist`;
CREATE TABLE `piclist` (
  `id` int(11) NOT NULL auto_increment,
  `path` varchar(255) NOT NULL default '',
  `thumpath` varchar(255) NOT NULL default '',
  `width` int(11) NOT NULL default '0',
  `height` int(11) NOT NULL default '0',
  `thwidth` int(11) NOT NULL default '0',
  `thheight` int(11) NOT NULL default '0',
  `size` int(11) NOT NULL default '0',
  `extid` int(11) default NULL,
  `spoiler` tinyint(1) default NULL,
  PRIMARY KEY  (`id`),
  KEY `extid` (`extid`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `piclist`
--

LOCK TABLES `piclist` WRITE;
/*!40000 ALTER TABLE `piclist` DISABLE KEYS */;
INSERT INTO `piclist` VALUES (1,'12133233454564820.jpg','12133233454564820s.jpg',270,366,184,250,77294,1,NULL),(2,'12133234748842640.rar','12133234748842640s.rar',0,0,128,128,10209,11,NULL),(3,'12133236809861880.rar','../generic/archive.png',0,0,128,128,10209,11,NULL),(4,'12133237653306200.torrent','../generic/archive.png',0,0,128,128,13336,16,NULL),(5,'12133242030796790.py','../generic/text.png',0,0,128,128,2588,24,NULL),(6,'12133500145660310.ico','12133500145660310s.jpg',128,128,128,128,82726,8,NULL),(7,'12133500445062080.ico','12133500445062080s.jpg',128,128,128,128,82726,8,NULL),(8,'12133502782532858.ico','12133502782532858s.jpg',128,128,128,128,82726,8,NULL),(9,'12133505064236720.png','12133505064236720s.png',1280,800,250,156,21000,5,NULL),(10,'12133506847454200.jpg','12133506847454200s.jpg',750,600,250,200,75209,1,NULL),(11,'12133508196732380.png','12133508196732380s.png',1280,1024,250,200,159429,5,NULL),(12,'12133512157899490.jpg','12133512157899490s.jpg',680,863,197,250,408484,1,NULL),(13,'12133574611674580.jpg','12133574611674580s.jpg',225,300,187,250,16651,1,NULL),(14,'12133576482248230.png','12133576482248230s.png',194,200,194,200,80049,5,NULL),(15,'12133821198079218.jpg','12133821198079218s.jpg',455,692,164,250,31723,1,NULL),(16,'12135091812161018.jpg','12135091812161018s.jpg',681,900,189,250,317990,1,NULL),(17,'12135412921136050.jpg','12135412921136050s.jpg',800,600,250,187,106649,1,NULL),(18,'12136337868147010.png','12136337868147010s.png',194,200,194,200,79679,5,NULL),(19,'12136346303483530.png','12136346303483530s.png',300,300,250,250,1644,5,NULL),(20,'12136351281304560.jpg','12136351281304560s.jpg',200,164,200,164,56155,1,NULL),(21,'12136359620100378.png','12136359620100378s.png',300,300,250,250,1820,5,NULL),(22,'12136803763928230.png','12136803763928230s.png',300,300,250,250,1971,5,NULL),(23,'12136806328982580.png','12136806328982580s.png',831,635,250,191,70242,5,NULL),(24,'12136806865493320.png','12136806865493320s.png',831,635,250,191,107515,5,NULL),(25,'12136974979614552.png','12136974979614552s.png',200,164,200,164,71028,5,NULL),(26,'12136982437422170.jpg','12136982437422170s.jpg',780,1157,168,250,317065,1,NULL),(27,'12137260251610178.jpg','12137260251610178s.jpg',900,1125,200,250,180853,1,NULL),(28,'12138526965952700.gif','12138526965952700s.gif',277,308,225,250,14510,3,NULL),(29,'12138596983520670.gif','12138596983520670s.gif',284,304,234,250,18964,3,NULL),(30,'12138597472979850.gif','12138597472979850s.gif',284,304,234,250,18964,3,NULL),(31,'12138743797387130.jpg','12138743797387130s.jpg',399,450,222,250,38878,1,NULL),(32,'12138893916973792.png','12138893916973792s.png',399,450,222,250,167591,5,NULL),(33,'12138897814589160.psd','12138897814589160s.jpg',1090,276,250,63,27470,10,NULL),(34,'12138899307924450.png','12138899307924450s.png',1090,276,250,63,27470,5,NULL),(35,'12138904201668342.png','12138904201668342s.png',194,200,194,200,80323,5,NULL);
/*!40000 ALTER TABLE `piclist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_tags`
--

DROP TABLE IF EXISTS `post_tags`;
CREATE TABLE `post_tags` (
  `post_id` int(11) default NULL,
  `tag_id` int(11) default NULL,
  `is_main` tinyint(1) default NULL,
  KEY `post_id` (`post_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `post_tags`
--

LOCK TABLES `post_tags` WRITE;
/*!40000 ALTER TABLE `post_tags` DISABLE KEYS */;
INSERT INTO `post_tags` VALUES (1,1,NULL),(5,2,NULL),(10,2,NULL),(17,2,NULL),(24,2,NULL),(25,2,NULL),(28,7,NULL),(29,2,NULL),(30,9,NULL),(31,9,NULL),(54,2,NULL),(60,2,NULL),(64,13,NULL),(70,2,NULL),(76,2,NULL),(101,16,NULL),(101,2,NULL),(103,18,NULL),(101,17,NULL),(110,2,NULL);
/*!40000 ALTER TABLE `post_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL auto_increment,
  `parentid` int(11) NOT NULL default '0',
  `message` text,
  `title` text,
  `sage` tinyint(1) default NULL,
  `sign` varchar(32) default NULL,
  `uid_number` int(11) default NULL,
  `picid` int(11) default NULL,
  `date` datetime NOT NULL default '0000-00-00 00:00:00',
  `last_date` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `picid` (`picid`)
) ENGINE=MyISAM AUTO_INCREMENT=112 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,-1,'Ð¢ÐµÑÑ‚ 1, Ð¿Ñ€Ð¾ÑÑ‚Ð¾ ÐºÐ°Ñ€Ñ‚Ð¸Ð½ÐºÐ°','',NULL,NULL,NULL,1,'2008-06-12 22:15:45','2008-06-13 07:44:21'),(2,1,'Ð¢ÐµÑÑ‚ 2, Ð°Ñ€Ñ…Ð¸Ð²','',NULL,NULL,NULL,2,'2008-06-12 22:17:54',NULL),(3,1,'Ð˜ ÐµÑ‰Ðµ Ñ€Ð°Ð·...','',NULL,NULL,NULL,3,'2008-06-12 22:21:20',NULL),(4,1,'','',NULL,NULL,NULL,4,'2008-06-12 22:22:45',NULL),(5,-1,'Ð§ÐµÐ³Ð¾-Ð½Ð¸Ð±ÑƒÐ´ÑŒ Ð»ÐµÐ²Ð¾Ðµ','',NULL,NULL,NULL,0,'2008-06-12 22:23:48','2008-06-15 08:25:14'),(6,1,'ÐœÐ¾Ð¶Ð½Ð¾ Ð¿Ð¾ÑÑ‚Ð¸Ñ‚ÑŒ Ð¸ÑÑ…Ð¾Ð´Ð½Ð¸ÐºÐ¸','',NULL,NULL,NULL,5,'2008-06-12 22:30:03',NULL),(7,5,'Ð‘Ð°Ð¼Ð¿','',NULL,NULL,NULL,0,'2008-06-12 23:11:12',NULL),(8,1,'Ð‘Ð°Ð¼Ð¿','',NULL,NULL,NULL,0,'2008-06-13 00:11:15',NULL),(9,5,'Ð˜ ÐµÑ‰Ðµ Ñ€Ð°Ð· Ð±Ð°Ð¼Ð¿...','',NULL,NULL,1,0,'2008-06-13 01:24:29',NULL),(10,-1,'ÐÐ¾Ð²Ñ‹Ð¹ Ñ‚Ñ€ÐµÐ´, Ð¿Ñ€Ð¾Ð²ÐµÑ€Ð¸Ñ‚ÑŒ Ñ€Ð°Ð±Ð¾Ñ‚Ñƒ Ð¿Ñ€Ð¸ Ð°Ð²Ñ‚Ð¾Ñ€Ð¸Ð·Ð°Ñ†Ð¸Ð¸','',NULL,NULL,1,0,'2008-06-13 01:26:24','2008-06-13 05:48:26'),(11,5,'Ð¡Ð°Ð¶Ð° Ð²Ð¾ Ð²ÑÐµ Ð¿Ð¾Ð»Ñ','Ð¡Ð°Ð¶Ð°!',1,NULL,1,0,'2008-06-13 02:04:50',NULL),(12,1,'Ð’Ð²ÐµÑ€Ñ…','',0,NULL,1,0,'2008-06-13 02:16:44',NULL),(13,5,'<span style=\"color:#FF0000;\">removed it, input should be filtered</span>','',1,NULL,1,0,'2008-06-13 03:01:25',NULL),(14,10,'Ð¡Ð°Ð¶Ð°','Ð¡Ð°Ð¶Ð°',1,NULL,2,0,'2008-06-13 04:16:57',NULL),(15,10,'Ð‘Ð°Ð¼Ð¿','',0,NULL,2,0,'2008-06-13 04:17:17',NULL),(16,10,'fsfds','',0,NULL,2,0,'2008-06-13 05:27:51',NULL),(17,-1,'Test','',NULL,NULL,1,6,'2008-06-13 05:40:14','2008-06-13 05:51:50'),(18,17,'Ð›ÑŽÑ‚Ñ‹Ð¹ Ð½ÐµÑÐ¼ÐµÑˆÐ½Ð¾Ð¹ Ð¿Ð¸Ð·Ð´ÐµÑ†','',0,NULL,1,7,'2008-06-13 05:40:44',NULL),(19,17,'Ð Ñ‚ÐµÐ¿ÐµÑ€ÑŒ ÑÐºÐ°Ð¶ÐµÑ‚ Ñ…ÑƒÐ¹','',0,NULL,1,0,'2008-06-13 05:44:20',NULL),(20,17,'','',0,NULL,1,8,'2008-06-13 05:44:38',NULL),(21,10,'','',0,NULL,2,9,'2008-06-13 05:48:26',NULL),(22,17,'sage','sage',1,NULL,5,10,'2008-06-13 05:51:24',NULL),(23,17,'bump','',0,NULL,5,0,'2008-06-13 05:51:50',NULL),(24,-1,'ÐÑ ?','',NULL,NULL,7,11,'2008-06-13 05:53:39','2008-06-13 05:53:39'),(25,-1,'test','',NULL,NULL,8,12,'2008-06-13 06:00:15','2008-06-13 06:00:15'),(26,1,'Ð¿ÑÐ´ Ð½Ðµ Ð¿Ð¾Ð»ÑƒÑ‡Ð¸Ð»Ð¾ÑÑŒ','',0,NULL,6,0,'2008-06-13 06:00:24',NULL),(27,1,'?','',0,NULL,10,13,'2008-06-13 07:44:21',NULL),(28,-1,'testpost ','test post in test board',NULL,NULL,9,0,'2008-06-13 07:47:08','2008-06-13 07:47:08'),(29,-1,'','',NULL,NULL,10,14,'2008-06-13 07:47:28','2008-06-19 11:47:00'),(30,-1,'','',NULL,NULL,12,0,'2008-06-13 14:25:20','2008-06-13 14:25:20'),(31,-1,'*test*\r\n**test**\r\ntest^H\r\n* test\r\n    test\r\n','test',NULL,NULL,12,15,'2008-06-13 14:35:19','2008-06-16 07:09:30'),(32,31,'test','',0,NULL,12,0,'2008-06-13 14:38:17',NULL),(33,31,'<p>\r\n<em></em></p>','',0,NULL,13,0,'2008-06-14 15:24:22',NULL),(34,31,'<p>\r\n<em></em></p>','',0,NULL,13,0,'2008-06-14 15:26:09',NULL),(35,31,'<p>\r\n<em></em></p>','',0,NULL,13,0,'2008-06-14 15:27:44',NULL),(36,31,'<p>\r\n</p>','',0,NULL,13,0,'2008-06-14 15:28:04',NULL),(37,31,'<p>\r\n<em></em></p>','',0,NULL,13,0,'2008-06-14 15:30:01',NULL),(38,31,'<p>\r\n<em></em></p>','',0,NULL,13,0,'2008-06-14 15:31:41',NULL),(39,31,'<p>\r\nzzzz<em>zzzz</em></p>','',0,NULL,13,0,'2008-06-14 15:34:15',NULL),(40,31,'<p>\r\nLol <em>test</em></p>','',0,NULL,13,0,'2008-06-14 15:35:40',NULL),(41,31,'<p>\r\n<a>&gt;&gt;31</a> moo</p>','',0,NULL,13,0,'2008-06-14 15:36:28',NULL),(42,31,'<p>\r\n<a href=\"31#i31\">&gt;&gt;31</a></p>\r\n<p>\r\n<span class=\"signature\">##<a href=\"31#i41\">41</a></span></p>','',0,NULL,13,0,'2008-06-14 15:50:45',NULL),(43,31,'<p>\r\n<a href=\"31#i31\">&gt;&gt;31</a></p>\r\n<p>\r\n<span class=\"signature\">##<a href=\"31#i41\">41</a></span></p>','',0,NULL,13,0,'2008-06-14 15:54:08',NULL),(44,31,'<blockquote>&gt; \r\n<a href=\"31#i31\">&gt;&gt;31</a><br />&gt; \r\nThis is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span><br />&gt; \r\nWe <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong><br />&gt; \r\nEven liek <strong><em>this</em></strong><br />&gt; \r\nAnd liek <strong><em>this</em></strong><blockquote>&gt; &gt; \r\n<a href=\"31#i31\">&gt;&gt;31</a><br />&gt; &gt; \r\nThis is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span><br />&gt; &gt; \r\nWe <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong><br />&gt; &gt; \r\nEven liek <strong><em>this</em></strong><br />&gt; &gt; \r\nAnd liek <strong><em>this</em></strong></blockquote></blockquote>\r\n<p>\r\n<a href=\"31#i31\">&gt;&gt;31</a><br />\r\nThis is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span><br />\r\nWe <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong><br />\r\nEven liek <strong><em>this</em></strong><br />\r\nAnd liek <strong><em>this</em></strong></p>\r\n<ul><li>\r\n  <a href=\"31#i31\">&gt;&gt;31</a></li><li>\r\n  This is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span></li><li>\r\n  We <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong></li><li>\r\n  Even liek <strong><em>this</em></strong></li><li>\r\n  And liek <strong><em>this</em></strong></li><li>\r\n    <a href=\"31#i31\">&gt;&gt;31</a></li><li>\r\n    This is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span></li><li>\r\n    We <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong></li><li>\r\n    Even liek <strong><em>this</em></strong></li><li>\r\n    And liek <strong><em>this</em></strong></li></ul><ol><li>\r\n  <a href=\"31#i31\">&gt;&gt;31</a></li><li>\r\n  This is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span></li><li>\r\n  We <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong></li><li>\r\n  Even liek <strong><em>this</em></strong></li><li>\r\n  And liek <strong><em>this</em></strong></li><li>\r\n    <a href=\"31#i31\">&gt;&gt;31</a></li><li>\r\n    This is a test block, with <strong>strong</strong> <strong>strong</strong>, <em>em</em> <em>em</em>, <del>strikeout</del> <del>strikeout</del>, <a href=\"31#i31\">&gt;&gt;31</a> and <span class=\"signature\">##<a href=\"31#i42\">42</a>,<a href=\"31#i41\">41</a></span></li><li>\r\n    We <strong>can <em>haev</em> nested</strong> <strong>elements <em>too</em></strong></li><li>\r\n    Even liek <strong><em>this</em></strong></li><li>\r\n    And liek <strong><em>this</em></strong></li></ol>\r\n<code>\r\n        >>31<br />\r\n        This is a test block, with **strong** __strong__, *em* _em_, strikeout^H^H^H^H^H^H^H^H^H strikeout^W, >>1000 and ##41,42<br />\r\n        We **can _haev_ nested** __elements *too*__<br />\r\n        Even liek ***this***<br />\r\n        And liek ___this___</code>\r\n','',0,NULL,13,0,'2008-06-14 15:57:41',NULL),(45,31,'<blockquote><blockquote>&gt; &gt; \r\n And liek this<blockquote>&gt; &gt; &gt; \r\n  <a href=\"31#i31\">&gt;&gt;31</a><blockquote>&gt; &gt; \r\nThis is a test block<blockquote>&gt; \r\nEven liek this</blockquote><p>\r\nTesting</p>','',0,NULL,13,0,'2008-06-14 16:13:13',NULL),(46,31,'<p>\r\n<strong>Ð¿Ñ€Ð¾Ð²ÐµÑ€ÐºÐ°</strong> <del>Ñ…ÑƒÐ¹</del></p>\r\n','',0,NULL,8,0,'2008-06-14 16:15:07',NULL),(47,31,'<p>\r\nÐšÑÑ‚Ð°Ñ‚Ð¸ <strong>Ñ€ÑƒÑÑÐºÐ¸Ð¹</strong> Ð½Ð°Ð´Ð¾ Ñ‚Ð¾Ð¶Ðµ Ð¿Ñ€Ð¾Ð²ÐµÑ€Ð¸Ñ‚ÑŒ.<br />\r\n<span class=\"signature\">##<a href=\"31#i44\">44</a></span>-ÐºÑƒÐ½</p>','',0,NULL,13,0,'2008-06-14 16:16:07',NULL),(48,31,'<p>\r\nÐ¿Ñ€Ð¾Ð²ÐµÑ€ÐºÐ° 2<br />\r\n<span class=\"signature\">##<a href=\"31#i46\">46</a></span></p>','',0,NULL,8,0,'2008-06-14 16:17:06',NULL),(49,31,'<p>\r\nÑ Ð¾Ð¿ Ð¸ ÑÐ¾ÑÑƒ Ñ…ÑƒÐ¸<br />\r\n</p>\r\n<p>\r\nÐ±Ð»Ð°Ð±Ð»Ð°Ð±Ð»Ð°</p>','',0,NULL,8,0,'2008-06-14 16:18:25',NULL),(50,31,'<blockquote><blockquote>&gt; &gt; \r\n And liek this<blockquote>&gt; &gt; &gt; \r\n  <a href=\"31#i31\">&gt;&gt;31</a></blockquote>&gt; &gt; \r\nThis is a test block</blockquote>&gt; \r\nEven liek this</blockquote><p>\r\nTesting</p>','',0,NULL,13,0,'2008-06-14 16:24:17',NULL),(51,29,'<p>\r\nÑ‚ÐµÑÑ‚</p>','',0,NULL,9,0,'2008-06-15 00:13:15',NULL),(52,29,'<p>\r\n123</p>','',0,NULL,9,0,'2008-06-15 00:13:20',NULL),(53,29,'<p>\r\n<span class=\"signature\">##<a href=\"29#i51\">51</a>,<a href=\"29#i52\">52</a></span></p>','',0,NULL,9,0,'2008-06-15 00:13:41',NULL),(54,-1,'<p>\r\n<strong>FUCK LOL YEAH!</strong></p>','',NULL,NULL,12,16,'2008-06-15 01:53:01','2008-06-15 02:06:53'),(55,54,'<p>\r\n<a href=\"54#i54\">&gt;&gt;54</a> TEST</p>','',0,NULL,12,0,'2008-06-15 01:54:49',NULL),(56,54,'<p>\r\n<a href=\"54#i55\">&gt;&gt;55</a> TEST</p>','',0,NULL,12,0,'2008-06-15 01:55:34',NULL),(57,54,'<p>\r\n54 TEST</p>','',0,NULL,12,0,'2008-06-15 01:55:49',NULL),(58,54,'','',0,NULL,12,0,'2008-06-15 02:06:53',NULL),(60,-1,'<p>\r\nÐ”Ð»Ñ Ð¿ÐµÑ€Ð»Ð¾Ñ„Ð°Ð³Ð¾Ð² Ð¸ Ð¿Ñ€Ð¾Ñ‡Ð¸Ñ… Ð¸Ð½Ð°ÐºÐ¾Ð¼Ñ‹ÑÐ»ÑÑ‰Ð¸Ñ…: <br />\r\nhttp://jaaa.ru/huitaba/<br />\r\nUID: 256256<br />\r\nÐ°Ð´Ð¼Ð¸Ð½ÐºÐ°: http://jaaa.ru/huitaba/board.pl?act=admin</p>\r\n<p>\r\nÐ¢ÐµÑÑ‚Ð¸Ñ€ÑƒÐµÐ¼ Ð¿Ð¾ÑÑ‚Ð¸Ð½Ð³, Ð¸Ð½Ð²Ð°Ð¹Ñ‚Ñ‹ Ð¸ Ð¿Ñ€Ð¾Ñ‡Ð¸Ðµ Ñ„Ð¸Ñ‡Ð¸.</p>','huitaba',NULL,NULL,12,17,'2008-06-15 10:48:12','2008-06-16 07:54:33'),(103,-1,'<p>\r\nÐŸÐµÑ€Ð²Ñ‹Ð¹ Ð¿Ð¾ÑÑ‚, Ð½Ñ!</p>','',NULL,NULL,13,NULL,'2008-06-19 07:59:20','2008-06-19 11:15:48'),(62,60,'','',0,NULL,9,0,'2008-06-16 07:54:33',NULL),(63,29,'<p>\r\nLol test<br />\r\nDrawn with <strong>Shi normal</strong> in 34 seconds, source <a href=\"29#i29\">&gt;&gt;29</a></p>','',0,NULL,13,18,'2008-06-16 12:29:46',NULL),(64,-1,'<p>\r\nÐžÐµÐºÐ°ÐºÐ¸ Ð¶Ðµ!<br />\r\nDrawn with <strong>Shi normal</strong> in 59 seconds</p>','',NULL,NULL,13,19,'2008-06-16 12:43:50','2008-06-17 01:26:39'),(65,29,'','',0,NULL,13,20,'2008-06-16 12:52:08',NULL),(66,64,'<p>\r\nÐ Ñ‡Ñ‚Ð¾, Ð½ÐµÐ´ÑƒÑ€Ð½Ð¾<br />\r\nDrawn with <strong>Shi normal</strong> in 25 seconds, source <a href=\"64#i64\">&gt;&gt;64</a></p>','',0,NULL,6,21,'2008-06-16 13:06:02',NULL),(67,64,'<p>\r\nÐ‘ÑƒÐ³Ð¾Ð³Ð°?</p>','',0,NULL,9,0,'2008-06-17 01:25:33',NULL),(68,64,'<p>\r\nÐ¤Ð°Ð°Ð°Ð°ÐºÐµÐ½ÑˆÐ¸Ñ‚<br />\r\nDrawn with <strong>Shi normal</strong> in 10 seconds, source <a href=\"64#i64\">&gt;&gt;64</a></p>','',0,NULL,9,22,'2008-06-17 01:26:16',NULL),(69,64,'<p>\r\nÐ¢Ð°Ð¼Ð±Ð½ÐµÐ¹Ð»Ñ‹ Ð½Ðµ Ñ„Ð¾Ñ€Ð¼Ð¸Ñ€ÑƒÑŽÑ‚ÑÑ</p>','',0,NULL,9,0,'2008-06-17 01:26:39',NULL),(70,-1,'<p>\r\n- Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ñ Ð¿Ð¾ÑÑ‚Ð¾Ð²<br />\r\n- Ð’Ð¾Ð·Ð²Ñ€Ð°Ñ‚Ð° Ðº Ð±Ð¾Ñ€Ð´Ðµ Ð¿Ñ€Ð¸ Ð¿Ð¾ÑÑ‚Ð¸Ð½Ð³Ðµ<br />\r\n- Ð¤Ð¾Ñ€Ð¼Ð¸Ñ€Ð¾Ð²Ð°Ð½Ð¸Ñ Ñ‚Ð°Ð¼Ð±Ð½ÐµÐ¹Ð»Ð¾Ð² Ð´Ð»Ñ Ð¾ÐµÐºÐ°Ðº<br />\r\n- Ð‘Ð»Ð¾ÐºÐ¸Ñ€Ð¾Ð²ÐºÐ¸ Ð¿ÑƒÑÑ‚Ñ‹Ñ… Ð¿Ð¾ÑÑ‚Ð¾Ð² Ð¸ Ð¾Ð¿-Ð¿Ð¾ÑÑ‚Ð¾Ð² Ð±ÐµÐ· ÐºÐ°Ñ€Ñ‚Ð¸Ð½ÐºÐ¸<br />\r\n- Ð¡Ð¿Ð¸ÑÐºÐ° Ñ‚ÑÐ³Ð¾Ð² ÑÐ²ÐµÑ€Ñ…Ñƒ Ð¸ ÑÐ½Ð¸Ð·Ñƒ<br />\r\n- Ð®Ð·ÐµÑ€Ñ‚ÐµÐ³Ð¾Ð²<br />\r\n- ÐžÐ±Ñ€ÐµÐ·Ð°Ð½Ð¸Ñ Ð´Ð»Ð¸Ð½Ð½Ñ‹Ñ… Ð¿Ð¾ÑÑ‚Ð¾Ð²<br />\r\n- Ð¡Ð²Ð¾Ñ€Ð°Ñ‡Ð¸Ð²Ð°Ð½Ð¸Ñ Ð±Ð¾Ð»ÑŒÑˆÐ¸Ñ… Ñ‚ÐµÐ¼<br />\r\n- Ð—Ð°Ð¿Ñ€ÐµÑ‚ Ð½Ð° Ð¿Ð¾ÑÑ‚Ð¸Ð½Ð³ Ñ Ð³Ð»Ð°Ð²Ð½Ð¾Ð¹. ÐÑƒ Ð¸Ð»Ð¸ Ð¿Ñ€Ð¸Ñ€Ð°Ð²Ð½Ð¸Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð¾ÑÑ‚Ð¸Ð½Ð³Ð° Ñ Ð³Ð»Ð°Ð²Ð½Ð¾Ð¹ Ðº Ð¿Ð¾ÑÑ‚Ð¸Ð½Ð³Ñƒ Ð² /b/</p>','Ð§Ð°Ð²Ð¾ Ð½ÐµÑ‚Ñƒ',NULL,NULL,9,23,'2008-06-17 01:30:32','2008-06-17 14:07:05'),(71,70,'\r\n<p>\r\nDrawn with <strong>Shi normal</strong> in 23 seconds, source <a href=\"70#i70\">&gt;&gt;70</a></p>','',0,NULL,9,24,'2008-06-17 01:31:26',NULL),(72,70,'<p>\r\nÐÐµÐ»ÑŒÐ·Ñ Ñ€Ð¸ÑÐ¾Ð²Ð°Ñ‚ÑŒ Ð¾ÐµÐºÐ°ÐºÑƒ Ð² Ð¾Ð¿ Ð¿Ð¾ÑÑ‚Ðµ...</p>','',0,NULL,9,0,'2008-06-17 01:32:39',NULL),(73,70,'<blockquote>&gt; \r\nÐÐµÐ»ÑŒÐ·Ñ Ñ€Ð¸ÑÐ¾Ð²Ð°Ñ‚ÑŒ Ð¾ÐµÐºÐ°ÐºÑƒ Ð² Ð¾Ð¿ Ð¿Ð¾ÑÑ‚Ðµ...</blockquote><p>\r\nÐœÐ¾Ð¶Ð½Ð¾. Ð¡Ð¼. http://newage3.com:5000/o/<br />\r\nÐŸÑ€Ð¾ÑÑ‚Ð¾ Ð½ÐµÑ‚ Ð¸Ð½Ñ‚ÐµÑ€Ñ„ÐµÐ¹ÑÐ° Ð´Ð»Ñ ÑÑ‚Ð¾Ð³Ð¾. (Ð½Ð°Ñ‡Ð°Ñ‚ÑŒ Ñ‚Ñ€ÐµÐ´ Ð¼Ð¾Ð¶Ð½Ð¾ Ñ ÑÑÑ‹Ð»ÐºÐ¸ http://newage3.com:5000/o/oekakiDraw)</p><blockquote>&gt; \r\n- Ð¤Ð¾Ñ€Ð¼Ð¸Ñ€Ð¾Ð²Ð°Ð½Ð¸Ñ Ñ‚Ð°Ð¼Ð±Ð½ÐµÐ¹Ð»Ð¾Ð² Ð´Ð»Ñ Ð¾ÐµÐºÐ°Ðº</blockquote><p>\r\nÐžÐ½Ð¸ Ð¸ ÑÐµÐ¹Ñ‡Ð°Ñ Ñ„Ð¾Ñ€Ð¼Ð¸Ñ€ÑƒÑŽÑ‚ÑÑ. ÐšÐ¾Ð´ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐ¸ ÐºÐ°Ñ€Ñ‚Ð¸Ð½Ð¾Ðº Ð½Ðµ Ð´ÐµÐ»Ð°ÐµÑ‚ Ñ€Ð°Ð·Ð»Ð¸Ñ‡Ð¸Ð¹ Ð¼ÐµÐ¶Ð´Ñƒ Ð¾ÐµÐºÐ°ÐºÐ¾Ð¹ Ð¸ Ð·Ð°Ð³Ñ€ÑƒÐ¶ÐµÐ½Ð½Ð¾Ð¹ ÐºÐ°Ñ€Ñ‚Ð¸Ð½ÐºÐ¾Ð¹</p>\r\n<p>\r\nÐžÑÑ‚Ð°Ð»ÑŒÐ½Ð¾Ðµ Ñ‰Ð°Ñ Ð¿Ñ€Ð¸Ð´ÐµÐ»Ð°ÑŽ</p>','',0,NULL,13,0,'2008-06-17 03:06:09',NULL),(74,70,'<p>\r\nÐÐ»ÑÐ¾, Ñ‡Ñ‚Ð¾Ð±Ñ‹ Ð½Ðµ Ð·Ð°Ð±Ñ‹Ñ‚ÑŒ,<br />\r\n- Ð”Ð¾Ð±Ð°Ð²Ð¸Ñ‚ÑŒ ÑÑÑ‹Ð»ÐºÐ¸ Ð² mark.def<br />\r\n- Ð”Ð¾Ð±Ð°Ð²Ð¸Ñ‚ÑŒ ÑÐ¿Ð¾Ð¹Ð»ÐµÑ€Ñ‹</p>','',0,NULL,13,0,'2008-06-17 04:25:22',NULL),(75,29,'\r\n<p>\r\nDrawn with <strong>Shi normal</strong> in 128 seconds, source <a href=\"29#i65\">&gt;&gt;65</a></p>','',0,NULL,9,25,'2008-06-17 06:11:37',NULL),(76,-1,'','',NULL,NULL,13,26,'2008-06-17 06:24:03','2008-06-17 06:24:03'),(77,70,'<p>\r\nÐÑƒÐ¶Ð½Ð° Ð°Ð²Ñ‚Ð¾Ð»Ð¾Ñ‡ÐºÐ° ÑƒÐ¸Ð´Ð° Ð¿Ñ€Ð¸ 5-10 Ð¿Ð¾ÑÑ‚Ð¾Ð² Ð² Ð¼Ð¸Ð½ÑƒÑ‚Ñƒ.</p>','',0,NULL,9,0,'2008-06-17 06:52:24',NULL),(78,70,'<p>\r\n- Ñ„Ð¸Ð»ÑŒÑ‚Ñ€, Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÑŽÑ‰Ð¸Ð¹ Ð²ÑÐµ Ñ‚Ñ€ÐµÐ´Ñ‹ Ð±ÐµÐ· Ñ‚ÐµÐ³Ð¾Ð², Ð±ÑƒÐ´Ðµ Ñ‚Ð°ÐºÐ¸Ðµ ÑÐ»ÑƒÑ‡Ð°Ñ‚ÑŒÑÑ.<br />\r\n- ÑÐµÐ¹Ñ‡Ð°Ñ Ð¿Ð¾Ð¿Ñ‹Ñ‚ÐºÐ° Ð¸ÑÐ¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÑŒ [Draw] Ð¿Ñ€Ð¸Ð²Ð¾Ð´Ð¸Ñ‚ Ðº 404</p>','',0,NULL,14,0,'2008-06-17 13:52:07',NULL),(79,70,'<p>\r\nÐžÐµÐºÐ°ÐºÐ° Ð¿Ð¾Ñ‡Ð¸Ð½ÐµÐ½Ð°.</p>','',0,NULL,14,27,'2008-06-17 14:07:05',NULL),(80,29,'<p>\r\nMany posts, 1</p>','',0,NULL,13,0,'2008-06-18 13:47:38',NULL),(81,29,'<p>\r\nMany posts, 2</p>','',0,NULL,13,0,'2008-06-18 13:47:46',NULL),(82,29,'<p>\r\nMany posts, 3</p>','',0,NULL,13,0,'2008-06-18 13:47:50',NULL),(110,-1,'<p>\r\nÐ£ Ð½Ð¸Ñ… Ñ‚Ð°Ð¼ ÐºÑ€ÑƒÐ³Ð¾Ð¼ Ð½Ð°Ñ€ÐºÐ¾Ð¼Ð°Ð½Ñ‹!</p>','',NULL,NULL,9,34,'2008-06-19 11:38:50','2008-06-19 11:38:50'),(107,103,'<p>\r\n<huita</huita</p>','',0,NULL,9,NULL,'2008-06-19 11:15:48',NULL),(86,29,'<p>\r\nMany posts, 7</p>','',0,NULL,13,0,'2008-06-18 13:48:11',NULL),(102,101,'<span style=\"color:#FF0000;\">deleted</span>','',0,NULL,9,NULL,'2008-06-19 07:25:53',NULL),(89,29,'<p>\r\nfsdfa</p>','',0,NULL,9,0,'2008-06-18 13:57:53',NULL),(90,29,'<p>\r\nÑÑ‚Ð¾Ð¼Ñƒ Ñ‚Ñ€ÐµÐ´Ñƒ Ð½ÐµÑ…Ð²Ð°Ñ‚Ð°Ñ‚</p>','',0,NULL,6,0,'2008-06-18 18:31:29',NULL),(91,29,'<p>\r\nÐ»ÑŽÑ‚Ð¾Ð±ÐµÑˆÐµÐ½Ð¾Ð½ÐµÑ…Ð²Ð°Ñ‚Ð°Ñ‚<br />\r\n<span class=\"signature\">##<a href=\"29#i90\">90</a></span></p>','',0,NULL,6,0,'2008-06-18 18:31:58',NULL),(92,29,'<p>\r\nÑ‚Ð°ÐºÐ¸ Ð´Ð°<br />\r\n89</p>','',0,NULL,6,0,'2008-06-18 18:32:15',NULL),(93,29,'<p>\r\nTesting posting and gb2</p>','',0,NULL,13,0,'2008-06-19 01:14:37',NULL),(105,103,'<p>\r\n<binjection</b</p>','',0,NULL,9,NULL,'2008-06-19 09:49:14',NULL),(111,29,'\r\n<p>\r\nDrawn with <strong>Shi normal</strong> in 178 seconds, source <a href=\"29#i29\">&gt;&gt;29</a></p>','',0,NULL,15,35,'2008-06-19 11:47:00',NULL),(101,-1,'<p>\r\nÐšÑ€Ð¾ÑÑÐ¿Ð¾ÑÑ‚ Ð² /b/, /nigras/ Ð¸ /gg/</p>','',NULL,NULL,13,31,'2008-06-19 07:19:39','2008-06-19 11:29:51');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_options`
--

DROP TABLE IF EXISTS `tag_options`;
CREATE TABLE `tag_options` (
  `id` int(11) NOT NULL auto_increment,
  `tag_id` int(11) default NULL,
  `comment` varchar(255) default NULL,
  `section_id` int(11) NOT NULL default '0',
  `persistent` tinyint(1) NOT NULL default '0',
  `imageless_thread` tinyint(1) NOT NULL default '0',
  `imageless_post` tinyint(1) NOT NULL default '0',
  `images` tinyint(1) NOT NULL default '0',
  `max_fsize` int(11) NOT NULL default '0',
  `min_size` int(11) NOT NULL default '0',
  `thumb_size` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tag_options`
--

LOCK TABLES `tag_options` WRITE;
/*!40000 ALTER TABLE `tag_options` DISABLE KEYS */;
INSERT INTO `tag_options` VALUES (1,1,NULL,5,1,0,0,1,2621440,100,250),(2,18,NULL,1,1,1,1,0,2621440,100,250),(3,2,NULL,2,1,0,1,1,2621440,50,250),(4,9,NULL,4,1,0,1,1,2621440,50,250),(5,13,'Oekaki',3,1,0,0,1,2621440,300,300),(6,19,NULL,2,1,1,1,1,2621440,50,250);
/*!40000 ALTER TABLE `tag_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL auto_increment,
  `tag` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (1,'rm'),(2,'b'),(7,'test'),(20,'(s+a)&b-ls'),(9,'a'),(19,'s'),(18,'d'),(13,'o'),(17,'gg'),(16,'nigras');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_options`
--

DROP TABLE IF EXISTS `user_options`;
CREATE TABLE `user_options` (
  `optid` int(11) NOT NULL auto_increment,
  `uid_number` int(11) default NULL,
  `threads_per_page` int(11) NOT NULL default '0',
  `replies_per_thread` int(11) NOT NULL default '0',
  `style` varchar(32) NOT NULL default '',
  `template` varchar(32) NOT NULL default '',
  `bantime` int(11) NOT NULL default '0',
  `banreason` text NOT NULL,
  PRIMARY KEY  (`optid`),
  KEY `uid_number` (`uid_number`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_options`
--

LOCK TABLES `user_options` WRITE;
/*!40000 ALTER TABLE `user_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid_number` int(11) NOT NULL auto_increment,
  `uid` varchar(128) NOT NULL default '',
  PRIMARY KEY  (`uid_number`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'c5f9dd6e5c5e04419b9b369e602bc4d0b627bb03bbbe7b7da6d992cadc785c3fedf4009323c52f9b48c443c5dc4b69e2101d515a8f3fc2edd4155843473ef0d6'),(2,'031f81e40c1f18ae36d2edc79e0bd4e26cbf3879279c083201e7283982c2d661bd6625267491985668ef9099b2947809dec5380227a5e26879e883f0a2e4e438'),(3,'9541bffb5c12c04ea1c136dcfbfa4bb5d6836b35731291d391bde626c1db670a3f546b6ef8644e4173ba9469f0ae891cafb7ae90b2a1603f48b9a0988355e8c2'),(4,'8446fc5f658d08f58ca8904e03a8a8a0d7c0ef3089a64758b607a1fa2c4fb98e47e6d5134bdadf3084c5b4714aea17a813501806fa39a639a920e3b0b03de479'),(5,'8446fc5f658d08f58ca8904e03a8a8a0d7c0ef3089a64758b607a1fa2c4fb98e47e6d5134bdadf3084c5b4714aea17a813501806fa39a639a920e3b0b03de479'),(6,'109514c75352cabf342e5fb6048e632c916e564ba63e138e8cf712852983a295b9ec2f4bdccde2ed6c98ca9b5393c833ce668a7d660089c69bf931b94a3e745e'),(7,'09782dbf9ba6139c7727b3023338b4cc8d63baea72581ba5977af087d958777f44c9af02b8dd177bcccd799794bef820fd439a8ee2ca685dfc053fa55c924046'),(8,'c9248ad6c4db8de2266830434009712cd49425632850282edbf2b103f50a6f945a0ad4390bd01f9c81cb8925d33465c27a35cdec614d663d9198285e462fd36c'),(9,'ee4f7b95ebd7f7a51499a18c1f3e131acfaeedee031bdcd1541c82200f392431956fada35ba3f0f76983637de29f026c8dbd478b256fc53af67867c7f44cb42b'),(10,'c80c1dd0909e96f7acc7109a2ffcc269e681852c244798340b7e5b938ba66e7341fda1cede07a0cf08dd1ab9467008d5ffd0a3f2fc0c898398b0958a7824f3d6'),(11,'b608c5f471b1d992908e3de932b5b0f13b743d0fc165383f07e780d317227aab752359f6001fcc8435b5a24ec4045faac5618b59fa3845620fbe42bb4210716d'),(12,'aa3fcbb28daea3f745dc34102ac7354f5dc259d4de1ec00f5d4da6c783da43f7d9fae59d01701c0d64a5971ec674984fcccf5897fc4da09600212f384c10a2da'),(13,'d8ea25e6613e3ed34d08fc4c076754ad7fee80c11b83fc45940c073361727ef72e1bb2fb55cc2ac7e651e4decaa4269fc52ff4457ad27a95e7f324c17220f1b4'),(14,'4e86eb7c491f7c555162dd2f2c02738e573aa9cbb866e571d8bccfdbc1d4364a66a4ac954b1df9774fa28e9777a9ba4bfe9d6363e67df831d5affcf1e2a48336'),(15,'b0e344e130201aec726866b25c225c18b1b34acf68e64420e2e2f7a9a6e599cd13d1ffcbfda4b0e1ee4d2feb0c68af7772daad91123d3b26b7b07a12b31f4ba3');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

