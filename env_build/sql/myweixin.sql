

CREATE TABLE  IF NOT EXISTS `access_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'the id of the access_token',
  `appid` varchar(128)  DEFAULT '',
  `appsecret` varchar(128)  DEFAULT '',
  `access_token` varchar(1000)  DEFAULT '',
  `update_time` TIMESTAMP  DEFAULT CURRENT_TIMESTAMP  COMMENT 'the update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


CREATE TABLE  IF NOT EXISTS `weather_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'the id of the weather_data',
  `city` varchar(32)  DEFAULT '',
  `data` varchar(1000)  DEFAULT '',
  `update_time` TIMESTAMP  DEFAULT CURRENT_TIMESTAMP  COMMENT 'the update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

