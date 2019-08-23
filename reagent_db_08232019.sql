-- MySQL dump 10.13  Distrib 8.0.16, for osx10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: reagent_db
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `component`
--

DROP TABLE IF EXISTS `component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `component` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `barcode` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `part_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lot_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `condition` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `kit_fk` int(11) DEFAULT NULL,
  `madereagent_fk` int(11) DEFAULT NULL,
  `copies` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kit_fk` (`kit_fk`),
  KEY `madereagent_fk` (`madereagent_fk`),
  CONSTRAINT `component_ibfk_1` FOREIGN KEY (`kit_fk`) REFERENCES `kit` (`id`),
  CONSTRAINT `component_ibfk_2` FOREIGN KEY (`madereagent_fk`) REFERENCES `made_reagent` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `component`
--

LOCK TABLES `component` WRITE;
/*!40000 ALTER TABLE `component` DISABLE KEYS */;
/*!40000 ALTER TABLE `component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kit`
--

DROP TABLE IF EXISTS `kit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `barcode` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `part_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lot_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `exp_date` datetime DEFAULT NULL,
  `date_entered` datetime DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `manufacturer_fk` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `manufacturer_fk` (`manufacturer_fk`),
  CONSTRAINT `kit_ibfk_1` FOREIGN KEY (`manufacturer_fk`) REFERENCES `manufacturer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kit`
--

LOCK TABLES `kit` WRITE;
/*!40000 ALTER TABLE `kit` DISABLE KEYS */;
/*!40000 ALTER TABLE `kit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `made_reagent`
--

DROP TABLE IF EXISTS `made_reagent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `made_reagent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `exp_date` datetime DEFAULT NULL,
  `date_entered` datetime DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `made_reagent`
--

LOCK TABLES `made_reagent` WRITE;
/*!40000 ALTER TABLE `made_reagent` DISABLE KEYS */;
/*!40000 ALTER TABLE `made_reagent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manufacturer`
--

DROP TABLE IF EXISTS `manufacturer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `manufacturer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `date_entered` datetime DEFAULT NULL,
  `barcode` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `part_num` int(11) DEFAULT NULL,
  `lot_num` int(11) DEFAULT NULL,
  `exp_date` int(11) DEFAULT NULL,
  `part_start` int(11) DEFAULT NULL,
  `part_end` int(11) DEFAULT NULL,
  `lot_start` int(11) DEFAULT NULL,
  `lot_end` int(11) DEFAULT NULL,
  `exp_date_start` int(11) DEFAULT NULL,
  `exp_date_end` int(11) DEFAULT NULL,
  `comp_barcode` int(11) DEFAULT NULL,
  `comp_part_num` int(11) DEFAULT NULL,
  `comp_lot_num` int(11) DEFAULT NULL,
  `compo_barcode` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `comp_part_start` int(11) DEFAULT NULL,
  `comp_part_end` int(11) DEFAULT NULL,
  `comp_lot_start` int(11) DEFAULT NULL,
  `comp_lot_end` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturer`
--

LOCK TABLES `manufacturer` WRITE;
/*!40000 ALTER TABLE `manufacturer` DISABLE KEYS */;
INSERT INTO `manufacturer` VALUES (1,'ProMega','2019-08-19 14:18:04','AS13101749502019/09',1,1,1,2,7,6,14,12,19,1,1,1,'123456789123456789',0,4,13,18);
/*!40000 ALTER TABLE `manufacturer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reagent`
--

DROP TABLE IF EXISTS `reagent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `reagent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `barcode` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `part_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lot_num` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `exp_date` datetime DEFAULT NULL,
  `date_entered` datetime DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `manufacturer_fk` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `manufacturer_fk` (`manufacturer_fk`),
  CONSTRAINT `reagent_ibfk_1` FOREIGN KEY (`manufacturer_fk`) REFERENCES `manufacturer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reagent`
--

LOCK TABLES `reagent` WRITE;
/*!40000 ALTER TABLE `reagent` DISABLE KEYS */;
/*!40000 ALTER TABLE `reagent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Irene','admin','1111');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-23  7:39:14
