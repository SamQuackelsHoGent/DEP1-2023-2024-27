CREATE TABLE `dimDatum` (
  `DateKey` integer PRIMARY KEY,
  `datumUSAFormaat` varchar(255),
  `datum` date,
  `datumint` integer,
  `seizoen` text,
  `speeldag` integer,
  `dagVanWeek` text,
  `dagVanWeekGetal` integer,
  `dagVanWeekKort` text,
  `kwartaal` integer
);

CREATE TABLE `dimPloeg` (
  `PloegKey` integer PRIMARY KEY,
  `stamnummer` integer,
  `naam` text
);

CREATE TABLE `dimTijd` (
  `TimeKey` integer PRIMARY KEY,
  `Time` varchar(255),
  `Time24` varchar(255),
  `Hour` integer,
  `HourName` integer,
  `MinuteKey` integer,
  `MinuteName` varchar(255),
  `Second` tinyint,
  `Hour24` tinyint,
  `AM` char
);

CREATE TABLE `dimWedstrijd` (
  `WedstrijdKey` integer PRIMARY KEY,
  `match_ID` integer,
  `dateKey` integer,
  `timeKey` integer,
  `huisploegKey` integer,
  `uitploegKey` integer,
  `standthuis` integer,
  `standuit` integer,
  `type` varchar(255)
);

CREATE TABLE `doelpunten` (
  `id` integer PRIMARY KEY,
  `matchKey` integer,
  `dateKey` integer,
  `tijdKey` integer,
  `GoalTimeKey` integer,
  `huisPloegKey` integer,
  `uitPloegKey` integer,
  `goalploegKey` integer,
  `huisstand` integer,
  `uitstand` integer,
  `eindHuisstand` integer,
  `eindUitstand` integer
);

CREATE TABLE `WeddenschapSource` (
  `WeddenschapKey` integer PRIMARY KEY,
  `WedstrijdKey` integer,
  `DatumWedstrijdKey` integer,
  `huisPloeg` integer,
  `uitPloeg` integer
);

CREATE TABLE `WeddenschapTarget` (
  `SID` integer PRIMARY KEY,
  `WeddenschapKey` integer,
  `DatumOpgehaaldKey` integer,
  `thuisWint` float,
  `gelijkspel` float,
  `uitWint` float,
  `TypeKey` integer,
  `meerDoelpunten` float,
  `minderDoelpunten` float,
  `betWebsitesKey` integer
);

CREATE TABLE `dimType` (
  `TypeKey` integer PRIMARY KEY,
  `betGoals` float
);

CREATE TABLE `Klassement` (
  `id` integer PRIMARY KEY,
  `seizoen` integer,
  `speeldag` integer,
  `stamnummer` integer,
  `roepnaam` varchar(255),
  `stand` integer,
  `gespeeldeMatchen` integer,
  `gewonnenMatchen` integer,
  `gelijkgespeeldeMatchen` integer,
  `verlorenMatchen` integer,
  `doelpunten` integer,
  `doelpuntenTegen` integer,
  `puntenVoor2Punten` integer,
  `puntenAchter2Punten` integer,
  `punten3Punten` integer,
  `puntenSaldo` integer
);

CREATE TABLE `betWebsites` (
  `betWebsitesKey` integer PRIMARY KEY,
  `website` varchar(255)
);

ALTER TABLE `dimWedstrijd` ADD FOREIGN KEY (`dateKey`) REFERENCES `dimDatum` (`DateKey`);

ALTER TABLE `dimWedstrijd` ADD FOREIGN KEY (`timeKey`) REFERENCES `dimTijd` (`TimeKey`);

ALTER TABLE `dimWedstrijd` ADD FOREIGN KEY (`huisploegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `dimWedstrijd` ADD FOREIGN KEY (`uitploegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`dateKey`) REFERENCES `dimDatum` (`DateKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`GoalTimeKey`) REFERENCES `dimTijd` (`TimeKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`matchKey`) REFERENCES `dimWedstrijd` (`WedstrijdKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`huisPloegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`uitPloegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `doelpunten` ADD FOREIGN KEY (`goalploegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`WedstrijdKey`) REFERENCES `dimWedstrijd` (`WedstrijdKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`DatumWedstrijdKey`) REFERENCES `dimDatum` (`DateKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`huisPloeg`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`uitPloeg`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`betWebsitesKey`) REFERENCES `betWebsites` (`betWebsitesKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`WeddenschapKey`) REFERENCES `WeddenschapSource` (`WeddenschapKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`DatumOpgehaaldKey`) REFERENCES `dimDatum` (`DateKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`TypeKey`) REFERENCES `dimType` (`TypeKey`);
