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
-- Table structure for table `manu_info`
--

DROP TABLE IF EXISTS `manu_info`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `manufacturer` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT 'n/a',
  
  `kit_part_num` tinyint(1) NOT NULL DEFAULT '1',
  `kit_lot_num` tinyint(1) NOT NULL DEFAULT '1',	
  `kit_exp_date` tinyint(1) NOT NULL DEFAULT '1',
  `kit_part_start` int(11) NOT NULL DEFAULT '-1',
  `kit_part_end` int(11) NOT NULL DEFAULT '-1',
  `kit_lot_start` int(11) NOT NULL DEFAULT '-1',
  `kit_lot_end` int(11) NOT NULL DEFAULT '-1',
  
  `comp_barcode` tinyint(1) NOT NULL DEFAULT '1',
  `part_num` tinyint(1) NOT NULL DEFAULT '1',
  `lot_num` tinyint(1) NOT NULL DEFAULT '1',
  `part_start` int(11) NOT NULL DEFAULT '-1',
  `part_end` int(11) NOT NULL DEFAULT '-1',
  `lot_start` int(11) NOT NULL DEFAULT '-1',
  `lot_end` int(11) NOT NULL DEFAULT '-1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `kit_master`
--

DROP TABLE IF EXISTS `kit_master`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kit_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `barcode` varchar(255) NOT NULL DEFAULT 'n/a',
  `part_num` int(255) DEFAULT NULL,
  `lot_num` int(255) DEFAULT NULL,
  `exp_date` date DEFAULT NULL,
  `quantity` int(255) DEFAULT NULL,
  `manu_fk` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `kit_comp`
--

DROP TABLE IF EXISTS `kit_comp`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kit_comp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comp_name` varchar(255) DEFAULT NULL,
  `comp_num` int(255) DEFAULT NULL,
  `part_num` int(255) DEFAULT NULL,
  `lot_num` int(255) DEFAULT NULL,
  `kit_fk` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;