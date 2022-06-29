-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 29, 2022 at 04:15 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gaminggeek`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
CREATE TABLE IF NOT EXISTS `items` (
  `itemId` varchar(10) COLLATE utf32_unicode_ci NOT NULL,
  `itemname` varchar(60) COLLATE utf32_unicode_ci DEFAULT NULL,
  `shortname` varchar(20) COLLATE utf32_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf32_unicode_ci,
  `Quantity` int(4) NOT NULL,
  `orginalprice` int(5) DEFAULT '0',
  `sellingprice` int(5) NOT NULL DEFAULT '0',
  `category` int(2) DEFAULT NULL,
  `hight` int(3) NOT NULL DEFAULT '0',
  `width` int(3) NOT NULL DEFAULT '0',
  `length` int(3) NOT NULL DEFAULT '0',
  `weight` int(4) NOT NULL DEFAULT '0',
  `minplayer` int(2) NOT NULL DEFAULT '1',
  `maxplayer` int(3) NOT NULL DEFAULT '1',
  `playtime` int(3) NOT NULL DEFAULT '30',
  `image1` varchar(100) COLLATE utf32_unicode_ci DEFAULT NULL,
  `image2` varchar(100) COLLATE utf32_unicode_ci DEFAULT NULL,
  `imag3` varchar(100) COLLATE utf32_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`itemId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf32 COLLATE=utf32_unicode_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`itemId`, `itemname`, `shortname`, `description`, `Quantity`, `orginalprice`, `sellingprice`, `category`, `hight`, `width`, `length`, `weight`, `minplayer`, `maxplayer`, `playtime`, `image1`, `image2`, `imag3`) VALUES
('bc005', 'Gobble and Fog', 'Hero Fight', 'A battle between two teams each team has to famous charectors', 3, 105, 220, 0, 10, 35, 45, 32, 2, 4, 30, '/media/pic5056685_euvKUHT.webp', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf32_unicode_ci NOT NULL,
  `password` varchar(512) COLLATE utf32_unicode_ci NOT NULL,
  `Name` varchar(60) COLLATE utf32_unicode_ci DEFAULT 'Flan',
  `email` varchar(80) COLLATE utf32_unicode_ci NOT NULL,
  `emailVerficationcode` varchar(6) COLLATE utf32_unicode_ci NOT NULL,
  `emailverification` tinyint(1) NOT NULL DEFAULT '0',
  `mainverification` tinyint(1) NOT NULL DEFAULT '0',
  `phone` varchar(10) COLLATE utf32_unicode_ci DEFAULT NULL,
  `PrivlageLevel` int(2) NOT NULL DEFAULT '0' COMMENT '0: Normal Vister, 1:admin, 2:Store Editer',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf32 COLLATE=utf32_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `username`, `password`, `Name`, `email`, `emailVerficationcode`, `emailverification`, `mainverification`, `phone`, `PrivlageLevel`) VALUES
(2, 'alibhp', 'ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413', 'Ali Albahrani', 'ali.albahrani@gmail.com', 'w6fb2J', 1, 1, '0477849182', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
