-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2023 at 02:21 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bughound`
--

-- --------------------------------------------------------

--
-- Table structure for table `areas`
--

CREATE TABLE `areas` (
  `area_id` int(11) NOT NULL,
  `prog_id` int(11) NOT NULL,
  `area` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `areas`
--

INSERT INTO `areas` (`area_id`, `prog_id`, `area`) VALUES
(15, 12, 'Logon'),
(16, 12, 'Start'),
(17, 12, 'DB Maintenance'),
(18, 12, 'Search'),
(19, 12, 'Insert New'),
(20, 12, 'Search Results'),
(21, 12, 'Add Edit Areas'),
(22, 12, 'Add Employees'),
(23, 12, 'Add Programs'),
(24, 12, 'view Bugs'),
(25, 13, 'Lexer'),
(26, 13, 'Parser'),
(27, 13, 'Code Generator'),
(28, 13, 'Linker'),
(29, 15, 'Lexer'),
(30, 15, 'Parser'),
(31, 15, 'Code Generator'),
(32, 15, 'Linker'),
(33, 14, 'Lexer'),
(34, 14, 'Parser'),
(35, 14, 'Code Generator'),
(36, 14, 'Linker'),
(37, 16, 'Lexer'),
(38, 16, 'Parser'),
(39, 16, 'Code Generator'),
(40, 16, 'Linker'),
(41, 17, 'Editor'),
(42, 17, 'Spell Checker'),
(43, 17, 'Dynodraw'),
(44, 17, 'Formulator'),
(45, 18, 'Menu'),
(46, 18, 'Router'),
(47, 18, 'Database'),
(48, 18, 'GUI'),
(1002, 18, 'new'),
(1003, 17, 'new');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `emp_id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `userlevel` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`emp_id`, `name`, `username`, `password`, `userlevel`) VALUES
(2, 'Timmy', 'timmy!', '123', 3),
(4, 'Hannah', 'smith', '789', 2),
(5, 'Johann Gomblepuddy', 'johanng', '111', 2),
(8, 'Prakash', 'smithp', '444', 2),
(1000, 'Chels k', 'chelfer', '123', 1),
(1001, '', 'ww', 'ww', 2);

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

CREATE TABLE `programs` (
  `prog_id` int(11) NOT NULL,
  `program` varchar(32) NOT NULL,
  `program_release` varchar(32) NOT NULL,
  `program_version` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`prog_id`, `program`, `program_release`, `program_version`) VALUES
(12, 'Bughound', '1', '1'),
(13, 'Visual Ada95', '1', '1'),
(14, 'Visual Ada95', '2', '1'),
(15, 'Visual Ada95', '1', '2'),
(16, 'Pascal Coder', '1', '1'),
(17, 'Word Writer 2019', '1', '1'),
(18, 'Mapstar 7', '1', '7');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`area_id`),
  ADD KEY `FK_progid` (`prog_id`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`emp_id`);

--
-- Indexes for table `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`prog_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `areas`
--
ALTER TABLE `areas`
  MODIFY `area_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1004;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `emp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1002;

--
-- AUTO_INCREMENT for table `programs`
--
ALTER TABLE `programs`
  MODIFY `prog_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1002;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `areas`
--
ALTER TABLE `areas`
  ADD CONSTRAINT `FK_progid` FOREIGN KEY (`prog_id`) REFERENCES `programs` (`prog_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
