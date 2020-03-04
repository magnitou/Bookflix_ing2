-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 17-07-2019 a las 18:56:33
-- Versión del servidor: 5.7.19-0ubuntu0.16.04.1-log
-- Versión de PHP: 7.0.18-0ubuntu0.16.04.1


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Base de datos: `grupo34`
--
-- --------------------------------------------------------

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `grupo34` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `grupo34`;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `tipo_instrumento`
--
CREATE TABLE `tipo_instrumento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE `genero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `nivel`
--

CREATE TABLE `nivel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preceptor`
--

CREATE TABLE `preceptor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------------------------------------
-- Estructura de tabla para la tabla `nucleo`
--

CREATE TABLE `nucleo`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `preceptor_nucleo`
--

CREATE TABLE `preceptor_nucleo` (
  `preceptor_id` int(11) NOT NULL,
  `nucleo_id` int(11) NOT NULL,
  PRIMARY KEY (preceptor_id, nucleo_id),
  CONSTRAINT FK_preceptor_id FOREIGN KEY (preceptor_id) REFERENCES preceptor(id),
  CONSTRAINT FK_nucleo_id FOREIGN KEY (nucleo_id) REFERENCES nucleo(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `localidad`
--

-- Consultar API de la Cátedra
-- https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `escuela`
--

CREATE TABLE `escuela` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci,
  `telefono` varchar(255) COLLATE utf8_unicode_ci,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `barrio`
--

CREATE TABLE `barrio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `lugar_nacimiento` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `nivel_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `escuela_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `responsable` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `barrio_id` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_nivel_id FOREIGN KEY (nivel_id) REFERENCES nivel(id),
  CONSTRAINT FK_genero_estudiante_id FOREIGN KEY (genero_id) REFERENCES genero(id),
  CONSTRAINT FK_escuela_id FOREIGN KEY (escuela_id) REFERENCES escuela(id),
  CONSTRAINT FK_barrio_id FOREIGN KEY (barrio_id) REFERENCES barrio(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable`
--

CREATE TABLE `responsable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_genero_responsable_id FOREIGN KEY (genero_id) REFERENCES genero(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `responsable_estudiante`
--

CREATE TABLE `responsable_estudiante` (
  `responsable_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  PRIMARY KEY (responsable_id, estudiante_id),
  CONSTRAINT FK_estudiante_id FOREIGN KEY (estudiante_id) REFERENCES estudiante(id),
  CONSTRAINT FK_responsable_id FOREIGN KEY (responsable_id) REFERENCES responsable(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docente`
--

CREATE TABLE `docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_genero_docente_id FOREIGN KEY (genero_id) REFERENCES genero(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE `taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre_corto` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo`
--

CREATE TABLE `ciclo_lectivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_ini` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `semestre` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `responsable_taller`
--

CREATE TABLE `docente_responsable_taller` (
  `docente_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL,
  PRIMARY KEY (docente_id, ciclo_lectivo_id, taller_id),
  CONSTRAINT FK_docente_responsable_taller_docente_id FOREIGN KEY (docente_id) REFERENCES docente(id),
  CONSTRAINT FK_docente_responsable_taller_ciclo_lectivo_id FOREIGN KEY (ciclo_lectivo_id) REFERENCES ciclo_lectivo(id),
  CONSTRAINT FK_docente_responsable_taller_taller_id FOREIGN KEY (taller_id) REFERENCES taller(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `ciclo_lectivo_taller`
--

CREATE TABLE `ciclo_lectivo_taller` (
  `taller_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  PRIMARY KEY (ciclo_lectivo_id, taller_id),
  CONSTRAINT FK_ciclo_lectivo_taller_ciclo_lectivo_id FOREIGN KEY (ciclo_lectivo_id) REFERENCES ciclo_lectivo(id),
  CONSTRAINT FK_ciclo_lectivo_taller_taller_id FOREIGN KEY (taller_id) REFERENCES taller(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `estudiante_taller`
--

CREATE TABLE `estudiante_taller` (
  `estudiante_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL,
  PRIMARY KEY (estudiante_id, ciclo_lectivo_id, taller_id),
  CONSTRAINT FK_estudiante_taller_id FOREIGN KEY (estudiante_id) REFERENCES estudiante(id),
  CONSTRAINT FK_estudiante_taller_ciclo_lectivo_id FOREIGN KEY (ciclo_lectivo_id) REFERENCES ciclo_lectivo(id),
  CONSTRAINT FK_estudiante_taller_taller_id FOREIGN KEY (taller_id) REFERENCES taller(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `asistencia_estudiante_taller`
--

CREATE TABLE `asistencia_estudiante_taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estudiante_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_asistencia_estudiante_id FOREIGN KEY (estudiante_id) REFERENCES estudiante(id),
  CONSTRAINT FK_asistencia_ciclo_lectivo_id FOREIGN KEY (ciclo_lectivo_id) REFERENCES ciclo_lectivo(id),
  CONSTRAINT FK_asistencia_taller_id FOREIGN KEY (taller_id) REFERENCES taller(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--
DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (2,'fede@gmail.com','fede','1234',1,19-11-20,19-11-20,'fede','Mozzon');
INSERT INTO `usuario` VALUES (1,'ivan@gmail.com','ivan','1234',1,19-11-20,19-11-20,'ivan','Mindlin');
INSERT INTO `usuario` VALUES (3,'lorenzo@gmail.com','lorenzo','1234',1,19-11-20,19-11-20,'lorenzo','Handula');
INSERT INTO `usuario` VALUES (4,'euge@gmail.com','chiquita','2222',0,19-12-22,19-12-22,'euge','Winschu');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--
DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Admin'),(2,'Docente'),(3,'Preceptor');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

CREATE TABLE `permiso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `permiso` WRITE;
/*!40000 ALTER TABLE `permiso` DISABLE KEYS */;
INSERT INTO `permiso` VALUES (1,'usuario_index'),(2,'usuario_new'),(3,'usuario_destroy'),(4,'usuario_update'),(5,'usuario_show'),(6,'usuario_activar'),(7,'usuario_desactivar'),(8,'usuario_asignar_rol'), (9,'configuracion_paginado'), (10,'configuracion_info'), (11, 'configuracion_habilitado'), (12, 'configuracion_usarInhabilitado'), (13, 'estudiantes_new'), (14, 'estudiantes_index'), (15, 'estudiantes_show'), (16, 'estudiantes_update'), (17, 'estudiantes_destroy'), (18, 'docentes_new'), (19, 'docentes_index'), (20, 'docentes_show'), (21, 'docentes_update'), (22, 'docentes_destroy'), (23, 'lectivo_new'), (24, 'lectivo_index'), (25, 'lectivo_show'), (26, 'lectivo_update'), (27, 'lectivo_destroy'), (28, 'instrumento_new'), (29, 'instrumento_index'), (30, 'instrumento_show'), (31, 'instrumento_update'), (32, 'instrumento_destroy'), (33, 'horario_index'), (34, 'horario_show'), (35, 'horario_new'), (36, 'horario_update'), (37, 'horario_destroy');
/*!40000 ALTER TABLE `permiso` ENABLE KEYS */;
UNLOCK TABLES;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `rol_tiene_permiso` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL,
  PRIMARY KEY (rol_id, permiso_id),
  CONSTRAINT FK_rol_id FOREIGN KEY (rol_id) REFERENCES rol(id),
  CONSTRAINT FK_permiso_id FOREIGN KEY (permiso_id) REFERENCES permiso(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




LOCK TABLES `rol_tiene_permiso` WRITE;
/*!40000 ALTER TABLE `rol_tiene_permiso` DISABLE KEYS */;
INSERT INTO `rol_tiene_permiso` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),
(2,1), (2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(3,1),(3,2),(3,3),(3,4),(3,5), (1, 12),
(1, 13), (1, 14), (1, 15), (1, 16), (1, 17),
(1, 18), (1, 19), (1, 20), (1, 21), (1, 22),
(1, 23), (1, 24), (1, 25), (1, 26), (1, 27),
(2, 14), (2, 15), (2, 16), (1, 28), (1, 29),
(3, 14), (3, 15), (3, 16), (1, 30), (1, 31),
(3, 19), (3, 20), (2, 29), (2, 30), (1, 32),
(3, 24), (3, 25), (1,33),(1,34),(1,35),(1,36),(1,37),(2,33),(2,34);

/*!40000 ALTER TABLE `rol_tiene_permiso` ENABLE KEYS */;
UNLOCK TABLES;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `usuario_tiene_rol` (
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL,
  PRIMARY KEY (usuario_id, rol_id),
  CONSTRAINT FK_usuario_utp_id FOREIGN KEY (usuario_id) REFERENCES usuario(id),
  CONSTRAINT FK_rol_utp_id FOREIGN KEY (rol_id) REFERENCES rol(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


LOCK TABLES `usuario_tiene_rol` WRITE;
/*!40000 ALTER TABLE `usuario_tiene_rol` DISABLE KEYS */;
INSERT INTO `usuario_tiene_rol` VALUES (1,1),(2,2),(3,1), (4,2);
/*!40000 ALTER TABLE `usuario_tiene_rol` ENABLE KEYS */;
UNLOCK TABLES;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instrumento`
--

CREATE TABLE `instrumento` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (id),
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_id` int(11) NOT NULL,
  `imagen` varchar(255), 
  `activo` tinyint(1) NOT NULL,
  CONSTRAINT FK_tipo_instrumento_id FOREIGN KEY (tipo_id) REFERENCES tipo_instrumento(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lista`
--

DROP TABLE IF EXISTS `lista`;

CREATE TABLE `lista`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `presente`
--

DROP TABLE IF EXISTS `presente`;

CREATE TABLE `presente`
(
    `fecha`         date    NOT NULL,
    `estudiante_id` int(11) NOT NULL,
    `lista_id`      int(11) NOT NULL,
    PRIMARY KEY (fecha, estudiante_id, lista_id),
    CONSTRAINT FK_estudiant_id FOREIGN KEY (estudiante_id) REFERENCES estudiante (id),
    CONSTRAINT FK_list_id FOREIGN KEY (lista_id) REFERENCES lista (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumno`
--

DROP TABLE IF EXISTS `alumno`;

CREATE TABLE `alumno`
(
    `estudiante_id` int(11) NOT NULL,
    `lista_id`      int(11) NOT NULL,
    PRIMARY KEY (estudiante_id, lista_id),
    CONSTRAINT FK_estudiantee_id FOREIGN KEY (estudiante_id) REFERENCES estudiante (id),
    CONSTRAINT FK_lista_id FOREIGN KEY (lista_id) REFERENCES lista (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesor`
--

DROP TABLE IF EXISTS `profesor`;

CREATE TABLE `profesor`
(
    `docente_id` int(11) NOT NULL,
    `lista_id`   int(11) NOT NULL,
    PRIMARY KEY (docente_id, lista_id),
    CONSTRAINT FK_docente_utp_id FOREIGN KEY (docente_id) REFERENCES docente (id),
    CONSTRAINT FK_listaa_id FOREIGN KEY (lista_id) REFERENCES lista (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
-- 



LOCK TABLES `taller` WRITE;
/*!40000 ALTER TABLE `taller` DISABLE KEYS */;
INSERT INTO `taller` VALUES (1,'Lenguaje Musical', 'LE'), (2, 'Ensamble', 'En'), (3, 'Expresion Corporal', 'EX'), (4, 'Historia del Arte', 'HA'), (5, 'Composicion', 'C');
/*!40000 ALTER TABLE `taller` ENABLE KEYS */;
UNLOCK TABLES;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

DROP TABLE IF EXISTS `configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad_elementos_pagina` int(5),
  `habilitado` tinyInt(1),
  `titulo` varchar (255),
  `descripcion` varchar (255),
  `mail_orquesta` varchar(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `configuracion` WRITE;
/*!40000 ALTER TABLE `configuracion` DISABLE KEYS */;
INSERT INTO `configuracion` VALUES (1,10,1,'Orquesta Escuela','La orquesta escuela trata con muchos chicos','escuelaOrquesta@orquesta.com');
/*!40000 ALTER TABLE `configuracion` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `paginado`;

CREATE TABLE `paginado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tamanio_paginado` int (5),
  `indice_actual` int (5),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

LOCK TABLES `paginado` WRITE;
INSERT INTO `paginado` VALUES (1, 5, 0);
UNLOCK TABLES;

DROP TABLE IF EXISTS `nucleo`;

CREATE TABLE `nucleo`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar (255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


LOCK TABLES `nucleo` WRITE;
INSERT INTO `nucleo` (id, nombre) VALUES (1, "jardin 904: 164 30 y 31"), (2,"Esc 501: Pascual Ruberto e/ 168 y 169"), (3,"CIC (centro Integración Complementaria) 169 y 33"), (4,"Parroquia San Miguel Arcángel: 63 y 124"), (5,"Centro Cultural Papa Francisco: 44 y 126 En La Plata (talleres y clases avanzados)"), (6,"Club Español: 6 e/ 53 y 54"), (7,"Teatro Argentino: 53 9 y 10");
UNLOCK TABLES;



DROP TABLE IF EXISTS `taller_nucleo_horario`;

CREATE TABLE `taller_nucleo_horario`(
                                        `taller_id` int(11) NOT NULL,
                                        `nucleo_id` int(11) NOT NULL,
                                        `dia`       varchar (255),
                                        `lista_id`  int(11) NOT NULL,
                                        PRIMARY KEY (taller_id, nucleo_id, dia, lista_id),
                                        CONSTRAINT FK_taller_utp_id FOREIGN KEY (taller_id) REFERENCES taller(id),
                                        CONSTRAINT FK_nucleo_utp_id FOREIGN KEY (nucleo_id) REFERENCES nucleo (id),
                                        CONSTRAINT FK_lista_utp_id FOREIGN KEY (lista_id) REFERENCES lista (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- TODO

-- revisar campos que pueden ser nulos (NO obligatorios)
-- armar tabla para mantener la historia de derivaciones de los pacientes

LOCK TABLES `genero` WRITE;
INSERT INTO `genero` (`id`, `nombre`) VALUES (1, 'Masculino');
INSERT INTO `genero` (`id`, `nombre`) VALUES (2, 'Femenino');
INSERT INTO `genero` (`id`, `nombre`) VALUES (3, 'Otro');
UNLOCK TABLES;

LOCK TABLES `tipo_instrumento` WRITE;
INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (1, 'Viento');
INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (2, 'Cuerda');
INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (3, 'Percusión');
UNLOCK TABLES;

LOCK TABLES `nivel` WRITE;
INSERT INTO `nivel` (`id`, `nombre`) VALUES (1, 'I');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (2, 'II');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (3, 'III');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (4, 'IV');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (5, 'V');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (6, 'VI');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (7, 'VII');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (8, 'VIII');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (9, 'IX');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (10, 'X');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (11, 'XI');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (12, 'XII');
UNLOCK TABLES;

LOCK TABLES `barrio` WRITE;
INSERT INTO `barrio` (`id`, `nombre`) VALUES (1, 'Barrio Náutico');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (2, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (3, 'Berisso');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (4, 'Barrio Solidaridad');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (5, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (6, 'Barrio Bco. Pcia.');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (7, 'Barrio J.B. Justo');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (8, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (9, 'El Carmen');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (10, 'El Labrador');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (11, 'Ensenada');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (12, 'La Hermosura');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (13, 'La PLata');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (14, 'Los Talas');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (15, 'Ringuelet');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (16, 'Tolosa');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (17, 'Villa Alba');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (18, 'Villa Arguello');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (19, 'Villa B. C');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (20, 'Villa Elvira');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (21, 'Villa Nueva');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (22, 'Villa Paula');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (23, 'Villa Progreso');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (24, 'Villa San Carlos');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (25, 'Villa Zula');
UNLOCK TABLES;

LOCK TABLES `escuela` WRITE;
INSERT INTO `escuela` (`nombre`) VALUES ('502');
INSERT INTO `escuela` (`nombre`) VALUES ('Albert Thomas');
INSERT INTO `escuela` (`nombre`) VALUES ('Anexa');
INSERT INTO `escuela` (`nombre`) VALUES ('Anexo T. Speroni');
INSERT INTO `escuela` (`nombre`) VALUES ('Basiliana');
INSERT INTO `escuela` (`nombre`) VALUES ('Basiliano');
INSERT INTO `escuela` (`nombre`) VALUES ('Bellas Artes');
INSERT INTO `escuela` (`nombre`) VALUES ('Canossiano');
INSERT INTO `escuela` (`nombre`) VALUES ('Castañeda');
INSERT INTO `escuela` (`nombre`) VALUES ('Col. Nacional');
INSERT INTO `escuela` (`nombre`) VALUES ('Conquista Cristiana');
INSERT INTO `escuela` (`nombre`) VALUES ('Dardo Rocha N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('E.E.M.N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('E.M. N°26');
INSERT INTO `escuela` (`nombre`) VALUES ('E.P. Municipal N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EE N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EEE N° 501');
INSERT INTO `escuela` (`nombre`) VALUES ('EEE N°501');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N° 1');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N° 26 L.P');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N°128');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N°2');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4 Berisso');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4 El Pino');
INSERT INTO `escuela` (`nombre`) VALUES ('EEST N° 1 bsso');
INSERT INTO `escuela` (`nombre`) VALUES ('EET Nº 1');
INSERT INTO `escuela` (`nombre`) VALUES ('EET Nº1');
INSERT INTO `escuela` (`nombre`) VALUES ('EGB N°25');
INSERT INTO `escuela` (`nombre`) VALUES ('EM N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EMM N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 1 L.P-');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 11');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 129');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 15');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 17');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 18');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 22');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 27');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 37 LP');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 43');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 65 La Plata');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 15');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 55');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 65');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 11');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 61');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 66');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 9');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 13');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 22');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 23');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 27');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 43');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 501');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 66');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°11');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°17');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°19');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°7');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC de Arte');
INSERT INTO `escuela` (`nombre`) VALUES ('ESS N° 4');
INSERT INTO `escuela` (`nombre`) VALUES ('Enseñanza Media');
INSERT INTO `escuela` (`nombre`) VALUES ('Especial N° 502');
INSERT INTO `escuela` (`nombre`) VALUES ('Estrada');
INSERT INTO `escuela` (`nombre`) VALUES ('FACULTAD');
INSERT INTO `escuela` (`nombre`) VALUES ('INDUSTRIAL');
INSERT INTO `escuela` (`nombre`) VALUES ('Italiana');
INSERT INTO `escuela` (`nombre`) VALUES ('J 904');
INSERT INTO `escuela` (`nombre`) VALUES ('J. Manuel Strada');
INSERT INTO `escuela` (`nombre`) VALUES ('Jacarandá');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín Euforion');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín N° 903');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín N° 907');
INSERT INTO `escuela` (`nombre`) VALUES ('JoaquinV.Gonzalez');
INSERT INTO `escuela` (`nombre`) VALUES ('Lola Mora sec');
INSERT INTO `escuela` (`nombre`) VALUES ('Lujan Sierra');
INSERT INTO `escuela` (`nombre`) VALUES ('MUNICIOAL 11');
INSERT INTO `escuela` (`nombre`) VALUES ('María Auxiliadora');
INSERT INTO `escuela` (`nombre`) VALUES ('María Reina');
INSERT INTO `escuela` (`nombre`) VALUES ('Media 2 España');
INSERT INTO `escuela` (`nombre`) VALUES ('Media N 1');
INSERT INTO `escuela` (`nombre`) VALUES ('Mercedita de S.Martin');
INSERT INTO `escuela` (`nombre`) VALUES ('Monseñor Alberti');
INSERT INTO `escuela` (`nombre`) VALUES ('Mtro Luis MKEY');
INSERT INTO `escuela` (`nombre`) VALUES ('Mñor. Rasore');
INSERT INTO `escuela` (`nombre`) VALUES ('N1 Francisco');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal 2');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal 3 LP');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal n 2');
INSERT INTO `escuela` (`nombre`) VALUES ('Ntra Sra Lourdes');
INSERT INTO `escuela` (`nombre`) VALUES ('Ntra. Sra. del Valle');
INSERT INTO `escuela` (`nombre`) VALUES ('PSICOLOGIA');
INSERT INTO `escuela` (`nombre`) VALUES ('Parroquial');
INSERT INTO `escuela` (`nombre`) VALUES ('Pasos del Libertedor');
INSERT INTO `escuela` (`nombre`) VALUES ('Ped 61');
INSERT INTO `escuela` (`nombre`) VALUES ('Pedagogica');
INSERT INTO `escuela` (`nombre`) VALUES ('SEC N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('SEC N°17');
INSERT INTO `escuela` (`nombre`) VALUES ('San Simón');
INSERT INTO `escuela` (`nombre`) VALUES ('Santa Rosa');
INSERT INTO `escuela` (`nombre`) VALUES ('Sra de Fátima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Margarita');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Ro. de Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Rosa');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Rosa Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta. R. de Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta. Rosa de lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 1');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 1 Berisso');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('UCALP');
INSERT INTO `escuela` (`nombre`) VALUES ('UNLP');
INSERT INTO `escuela` (`nombre`) VALUES ('UTN');
INSERT INTO `escuela` (`nombre`) VALUES ('Universitas');
UNLOCK TABLES;