create table DiskInfo(
  Id int not null auto_increment,
  Serial varchar(50) not null,
  Model  varchar(50) not null,
  ModelFamily varchar(50) not null,
  Capacity varchar(15) not null,
  CapacityBytes long not null,
  SectorSize int,
  PRIMARY KEY (Id)
);
create table DiskEntries(
  id int not null auto_increment,
  DiskID int not null,
  Percent_Life_Remain int not null,
  DiskTBW double not null,
  timestamp datetime not null,
  PRIMARY KEY (Id)  
);