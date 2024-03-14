CREATE TABLE `dimDatum` (
  `DatumKey` integer PRIMARY KEY,
  `volledigeDatum` date,
  `datumUSFormat` date,
  `datumInt` integer,
  `seizoen` text,
  `speeldag` integer,
  `naamMaandEngels` text,
  `naamMaandEngelsKort` text,
  `naamMaandNederlands` text,
  `naamMaandNederlandsKort` text,
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
  `TijdKey` integer PRIMARY KEY,
  `tijd` time,
  `tijd12U` time,
  `uur` integer,
  `minuut` integer,
  `seconde` integer,
  `tijdzone` integer,
  `tijdzoneUitgeschreven` text,
  `AMPM` text
);

CREATE TABLE `dimWedstrijd` (
  `WedstrijdKey` integer PRIMARY KEY
);

CREATE TABLE `Goal` (
  `id` integer PRIMARY KEY,
  `WedstrijdKey` integer,
  `DatumKey` integer,
  `GoalTijdKey` integer,
  `huisPloegKey` integer,
  `uitPloegKey` integer,
  `goalPloegKey` integer,
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
  `payoutPloeg1Wint` float,
  `payoutGelijkspel` float,
  `payoutPloeg2Wint` float,
  `TypeKey` integer,
  `payoutGoalsHogerDan` float,
  `payoutGoalsLagerDan` float,
  `payoutBeideScoren` float,
  `payoutBeideScorenNiet` float
);

CREATE TABLE `dimType` (
  `TypeKey` integer PRIMARY KEY,
  `betGoals` float
);

CREATE TABLE `Klassement` (
  `DatumKey` integer,
  `ploegKey` integer,
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

ALTER TABLE `Goal` ADD FOREIGN KEY (`DatumKey`) REFERENCES `dimDatum` (`DatumKey`);

ALTER TABLE `Goal` ADD FOREIGN KEY (`GoalTijdKey`) REFERENCES `dimTijd` (`TijdKey`);

ALTER TABLE `Goal` ADD FOREIGN KEY (`WedstrijdKey`) REFERENCES `dimWedstrijd` (`WedstrijdKey`);

ALTER TABLE `Goal` ADD FOREIGN KEY (`huisPloegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `Goal` ADD FOREIGN KEY (`uitPloegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `Goal` ADD FOREIGN KEY (`goalPloegKey`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`WedstrijdKey`) REFERENCES `dimWedstrijd` (`WedstrijdKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`DatumWedstrijdKey`) REFERENCES `dimDatum` (`DatumKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`huisPloeg`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapSource` ADD FOREIGN KEY (`uitPloeg`) REFERENCES `dimPloeg` (`PloegKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`WeddenschapKey`) REFERENCES `WeddenschapSource` (`WeddenschapKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`DatumOpgehaaldKey`) REFERENCES `dimDatum` (`DatumKey`);

ALTER TABLE `WeddenschapTarget` ADD FOREIGN KEY (`TypeKey`) REFERENCES `dimType` (`TypeKey`);

ALTER TABLE `Klassement` ADD FOREIGN KEY (`DatumKey`) REFERENCES `dimDatum` (`DatumKey`);

ALTER TABLE `Klassement` ADD FOREIGN KEY (`ploegKey`) REFERENCES `dimPloeg` (`PloegKey`);
