-- MySQL dump 10.13  Distrib 8.0.15, for macos10.14 (x86_64)
--
-- Host: localhost    Database: reagent_db
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_settings`
--

DROP TABLE IF EXISTS `admin_settings`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `admin_settings` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Copy_Amount` int(11) NOT NULL DEFAULT '15',
  `Admin_Code` varchar(45) NOT NULL DEFAULT 'pass123',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_settings`
--

LOCK TABLES `admin_settings` WRITE;
/*!40000 ALTER TABLE `admin_settings` DISABLE KEYS */;
INSERT INTO `admin_settings` VALUES (1,12,'password');
/*!40000 ALTER TABLE `admin_settings` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `manu_info`
--

DROP TABLE IF EXISTS `manu_info`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `manu_info` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Manufacturer` varchar(255) NOT NULL DEFAULT 'n/a',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `kit_comp`
--

DROP TABLE IF EXISTS `kit_comp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kit_comp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comp_name` varchar(255) DEFAULT NULL,
  `comp_num` int(255) DEFAULT NULL,
  `part_num` int(255) DEFAULT NULL,
  `lot_num` int(255) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `lab_expiry_date` date DEFAULT NULL,
  `master_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `kit_master`
--

DROP TABLE IF EXISTS `kit_master`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kit_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_master` varchar(255) DEFAULT NULL,
  `box_lot_barcode` varchar(255) NOT NULL DEFAULT 'n/a',
  `manufacturer_fk` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Dumping data for table `kit_master`
--

LOCK TABLES `kit_master` WRITE;
/*!40000 ALTER TABLE `kit_master` DISABLE KEYS */;
INSERT INTO `kit_master` VALUES (1,'Maxwell 16 FFPE Plus LEV DNA Purification Kit','AS11357996412019-10'),(2,'Maxwell 16 LEV simply RNA Blood Kit\r', 'n/a'),(3,'QIASymphony DSP DNA Midi Kit 96 v.1\r'),(4,'QIAamp Micro DNA Kit\r'),(5,'QIAamp MinElute Virus DNA from Plasma\r'),(6,'QIAgen Rneasy Kit\r'),(7,'QIAamp Circulating Nucleic Acid Kit\r'),(8,'QuantiFluor ONE'),(9,'InjectTest'),(10,'Injection Test 2'),(11,'rar'),(12,'newkit');
/*!40000 ALTER TABLE `kit_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rea_master`
--

DROP TABLE IF EXISTS `rea_master`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rea_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_master` varchar(255) DEFAULT NULL,
  `box_lot_barcode` varchar(255) NOT NULL DEFAULT 'n/a',
  `manufacturer_fk` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-24 13:59:30
