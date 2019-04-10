-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主機: 127.0.0.1
-- 產生時間： 2019 年 04 月 05 日 09:41
-- 伺服器版本: 10.1.35-MariaDB
-- PHP 版本： 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `nba`
--

-- --------------------------------------------------------

--
-- 資料表結構 `admin`
--

CREATE TABLE `admin` (
  `adid` int(11) NOT NULL,
  `adname` varchar(100) NOT NULL,
  `adpw` varchar(100) NOT NULL,
  `adrole` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `admin`
--

INSERT INTO `admin` (`adid`, `adname`, `adpw`, `adrole`) VALUES
(1, 'admin', 'admin', 'boss'),
(2, 'qwert', 'qwert', 'maintainer');

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `oid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `mobile` int(11) NOT NULL,
  `place` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `orders`
--

INSERT INTO `orders` (`oid`, `uid`, `pid`, `name`, `mobile`, `place`, `quantity`, `date`) VALUES
(3, 3, 1, 'asdfg', 87531827, 'Hong Kongljhiuytfi75', 5, '2019-04-12 11:55:57');

-- --------------------------------------------------------

--
-- 資料表結構 `products`
--

CREATE TABLE `products` (
  `pid` int(11) NOT NULL,
  `pname` varchar(200) NOT NULL,
  `pdetail` varchar(200) NOT NULL,
  `pprice` float NOT NULL,
  `ptype` varchar(50) NOT NULL,
  `plink` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `products`
--

INSERT INTO `products` (`pid`, `pname`, `pdetail`, `pprice`, `ptype`, `plink`) VALUES
(1, 'NIKE SWGMN Stephen Curry', 'NIKE DRI-FIT moisture wicking material, cool and comfortable.The double-knit mesh fabric is not only durable and light, but also keeps cool.Twill material stamped name and number.', 465, 'tshirt', 't1.jpg'),
(2, 'nba black', 'asdivybauisvydiakujvhsujydvfgsgfdsdf', 300, 'tshirt', 't2.jpg'),
(3, 'nba 3', 'asdaksdhvakjdsyfvkjagsvdkajhvsed', 690, 'tshirt', 't3.jpg'),
(4, 'tshirt4', 'KD', 399, 'tshirt', 't4.jpg'),
(5, 'Golden State Warriors Nike Association Edition Swingman Men\'s NBA Shorts(Clearance)', 'Golden State Warriors Nike Association Edition Swingman\r\nMen\'s NBA Shorts\r\nYOUR TEAM. YOUR COLORS.\r\nInspired by the authentic NBA shorts, the Golden State Warriors Nike Association Edition Swingman Me', 499.99, 'shorts', 's1.png'),
(6, 'Golden State Warriors Nike Men\'s Practice Shorts(Clearance)', 'DRI-FIT VISUALLY MIRRORS THE OFFICIAL PRACTICE SHORT WITH ICONIC VENT DETAIL, TEAM COLOR SIDE PANELS AND LOGO TAILORED FIT, LIGHT-WEIGHT MESH MATERIAL BASKETBALL', 314, 'shorts', 's2.png');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `useremail` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `userpw` varchar(100) NOT NULL,
  `useraddress` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `users`
--

INSERT INTO `users` (`userid`, `useremail`, `username`, `userpw`, `useraddress`) VALUES
(1, 'qwe@qw.qwe', 'qwe', 'qweqwe', 'qwe123'),
(2, 'qweasd@asd.asd', 'asdqwe', 'asdasd', 'asdasd'),
(3, 'www@www.www', 'www', 'wwwwww', 'wwwwwww'),
(4, 'jjj@jjj.jjj', 'jjj', 'jjjjjj', 'jjjjjj');

--
-- 已匯出資料表的索引
--

--
-- 資料表索引 `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adid`);

--
-- 資料表索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`oid`);

--
-- 資料表索引 `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`pid`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- 在匯出的資料表使用 AUTO_INCREMENT
--

--
-- 使用資料表 AUTO_INCREMENT `admin`
--
ALTER TABLE `admin`
  MODIFY `adid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表 AUTO_INCREMENT `orders`
--
ALTER TABLE `orders`
  MODIFY `oid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用資料表 AUTO_INCREMENT `products`
--
ALTER TABLE `products`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表 AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
