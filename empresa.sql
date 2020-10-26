-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-10-2020 a las 18:22:28
-- Versión del servidor: 10.4.14-MariaDB
-- Versión de PHP: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empresa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `admin`
--

INSERT INTO `admin` (`id`, `user`, `password`) VALUES
(1, 'johan', '1234'),
(2, 'Leonardo', 'arx160A1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL COMMENT 'Almacena la descripción del producto',
  `estado` varchar(1) DEFAULT NULL COMMENT 'Define si la categoria esta activa o no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Almacena la información de las categorias de los productos de la empresa';

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id`, `descripcion`, `estado`) VALUES
(0, 'Desayuno Sorpresa', '1'),
(1, 'Detalle Personalizado', '1'),
(2, 'Arreglo Floral', '1'),
(3, 'Caja Dulcera', '1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresa`
--

CREATE TABLE `empresa` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL COMMENT 'Almacena el nombre de la empresa',
  `quienessomos` varchar(500) DEFAULT NULL COMMENT 'Almacena la información de la empresa',
  `emailcontacto` varchar(50) DEFAULT NULL COMMENT 'Almacena el email al cual se enviaran los contactos',
  `direccion` varchar(200) DEFAULT NULL COMMENT 'Almacena la dirección de',
  `telefonocontacto` varchar(20) DEFAULT NULL,
  `facebook` varchar(100) DEFAULT NULL,
  `twitter` varchar(100) DEFAULT NULL,
  `instagram` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Almacena la información de la empresa.  Incluye todo lo referente a la configuración de la empresa.';

--
-- Volcado de datos para la tabla `empresa`
--

INSERT INTO `empresa` (`id`, `nombre`, `quienessomos`, `emailcontacto`, `direccion`, `telefonocontacto`, `facebook`, `twitter`, `instagram`) VALUES
(0, 'Detalles Dulce Regalo', 'Detalles Dulce Regalo es una empresa Cucuteña creada por 2 mujeres, visionarias que desde inicios del 2020 busca consolidarse como un referente en el mercado On-line de los Regalos y Detalles tipo experiencia.', '#', '#', '3223799990', '#', '#', 'https://www.instagram.com/detallesdulceregalo/');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `referencia` varchar(20) DEFAULT NULL COMMENT 'Referencia de los productos',
  `nombre` varchar(100) DEFAULT NULL COMMENT 'Nombre del producto',
  `descripcioncorta` varchar(250) DEFAULT NULL COMMENT 'Una descripcion corta del producto',
  `detalle` text DEFAULT NULL COMMENT 'Detalle extenso de la información del producto',
  `valor` decimal(10,2) DEFAULT NULL COMMENT 'Precio del producto',
  `imagen` varchar(255) NOT NULL,
  `categoria_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Almacena la información del producto';

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `referencia`, `nombre`, `descripcioncorta`, `detalle`, `valor`, `imagen`, `categoria_id`) VALUES
(8, '56465263', 'Desayuno Pony', 'Desayuno', 'Con un pony', '55000.00', 'detalle9.PNG', 0),
(9, '54654', 'Caja Sorpresa', 'Una caja', 'Con sorpresa', '5465132.00', 'detalle3.PNG', 3),
(10, '74557', 'Flores con Chocolates', 'Flores', 'con chocolates', '23651.00', 'detalle6.PNG', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `empresa`
--
ALTER TABLE `empresa`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `IXFK_producto_categoria` (`categoria_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `FK_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
