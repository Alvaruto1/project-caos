DELETE FROM `users`;
DELETE FROM `tokens`;
CREATE TABLE IF NOT EXISTS `tokens` (  `idtokens` int(11) NOT NULL AUTO_INCREMENT,  `value` varchar(45) DEFAULT NULL,  `date` datetime DEFAULT NULL,  PRIMARY KEY (`idtokens`)) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;
LOCK TABLES `tokens` WRITE;
INSERT INTO `tokens` VALUES (7,'-3951157336649051457','2019-12-31 12:43:48'),(8,'2818862320580395273','2019-12-11 21:15:39'),(9,'2989869777380230908','2019-12-11 21:21:53'),(10,'-1830859156996423279','2019-12-11 22:36:37'),(11,'2835662938604496423','2019-12-12 17:09:26'),(12,'3067293409087052973','2019-12-12 17:09:31'),(13,'-1200677666242653942','2019-12-12 17:09:41'),(14,'7688377309094510949','2019-12-12 17:20:08'),(32,'6625690283589693766','2019-12-30 21:37:30'),(33,'6788529533548622314','2019-12-30 21:38:19'),(34,'-1866332570585614148','2019-12-30 21:48:58'),(35,'3814772612186160506','2019-12-30 21:49:47'),(36,'-875120912215179457','2019-12-30 21:52:15'),(37,'-4825827863384257993','2019-12-30 21:52:38'),(38,'-3691534148393473981','2019-12-30 22:21:48'),(39,'-6918729444502293333','2019-12-30 21:55:16'),(43,'5714753284186196400','2019-12-30 22:00:12'),(44,'5227657874005963335','2019-12-30 22:01:05'),(46,'7647507266479205650','2019-12-30 22:03:19'),(48,'-4589254066667843820','2019-12-30 22:16:21'),(49,'-7143686822074890154','2019-12-30 22:17:01'),(50,'5362896939188917672','2019-12-30 22:17:52'),(51,'-3711007709073928524','2019-12-30 22:22:41'),(53,'4550690156069806629','2019-12-30 22:23:00'),(54,'-7376026359238294159','2019-12-31 13:20:33'),(56,'5221231761468402907','2019-12-30 22:45:09'),(58,'-3971971773383335526','2019-12-30 22:49:28'),(59,'-2975054696556361295','2019-12-31 12:06:48'),(60,'-8350825931677721735','2019-12-31 12:18:02'),(62,'8747001208661494712','2019-12-31 13:16:49');
UNLOCK TABLES;
CREATE TABLE IF NOT EXISTS `users` (  `idusers` int(11) NOT NULL AUTO_INCREMENT,  `email` varchar(45) DEFAULT NULL,  `password` varchar(45) DEFAULT NULL,  `idtoken` int(11) DEFAULT NULL,  PRIMARY KEY (`idusers`),  UNIQUE KEY `email_UNIQUE` (`email`),  KEY `fk_users_1_idx` (`idtoken`),  CONSTRAINT `fk_users_1` FOREIGN KEY (`idtoken`) REFERENCES `tokens` (`idtokens`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;
LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (7,'alvaruto58@gmail.com','123456',7),(9,'alvaruto2@gmail.com','123456',9),(10,'alvaruto4@gmail.com','123456',10),(14,'alvaruto5@gmail.com','123456',14),(38,'alvaruto10@gmail.com','1234567',38),(43,'alvaruto11@gmail.com','123456',43),(44,'alvaruto12@gmail.com','123',44),(46,'alvaruto13@gmail.com','12345',46),(48,'alvaruto16@gmail.com','123456',48),(49,'alvaruto18@gmail.com','123456',49),(50,'alvaruto20@gmail.com','123456',50),(51,'liz@gmasil.com','123456',51),(53,'liz2@gmasil.com','1234567',53),(54,'liz3@gmasil.com','1234567',54),(56,'liz9@gmasil.com','123456',56),(58,'liz21@gmasil.com','123456',58),(60,'alvaruto48@gmail.com','123456',60),(62,'blvaruto@gmail.com','123456',62);
UNLOCK TABLES;