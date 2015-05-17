#create database squawka;

create table IF NOT EXISTS tbMatchEvent(
    iEventID bigint unsigned  not null auto_increment comment '事件ID',
    iMatchID bigint unsigned not null default 0 comment '比赛ID',
    iMins int unsigned not null default 0 comment '事件发生时间分钟',
    iMinsec int unsigned not null default 0 comment '事件发生时间秒',
    iSecs int unsigned not null default 0 comment '事件发生时间分钟内的秒',
    iInjurytime_play BOOLEAN not null default 0 comment '0常规时间，1补时',
    iPlayer1ID int unsigned not null default 0 comment '队员1ID',
    iPlayer2ID int unsigned not null default 0 comment '队员2ID',
    iType int unsigned not null default 0 comment '统计类型 1 swapplayers，2 goal_keeping，3 head_duals，4 interceptions，5 clearances，6 all_passes，7 tackles，8 crosses，9 corners，10 offside，11 keepersweeper， 12 oneonones，13 setpieces，14 takeons，15 fouls，16 cards，17 blocked_events， 18 extra_heat_maps， 19 balls_out',
    szActionType varchar(128) default '' comment '动作类型',
    szType varchar(128) default '' comment '动作完成类型',
    iTeamID int unsigned not null default 0 comment '队伍ID',
    szEventContent text not null comment '事件详细内容',
    primary key (`iEventID`, `iMatchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='比赛事件表';

create table IF NOT EXISTS tbMatchInfo(
    iMatchID bigint unsigned not null default 0 comment '比赛ID',
    tStart varchar(512) not null default '' comment '开始时间',
    iHomeTeamID int unsigned not null default 0 comment '主队ID',
    iAwayTeamID int unsigned not null default 0 comment '客队ID',
    iHomeScore int unsigned not null default 0 comment '主队得分',
    iAwayScore int unsigned not null default 0 comment '客队得分',
    primary key (`iMatchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='比赛信息表';

create table IF NOT EXISTS tbPlayerInfo(
    iPlayerID int unsigned not null default 0 comment '队员ID',
    iTeamID int unsigned not null default 0 comment '球队ID',
    szFirstName varchar(128) default '' comment '球员first name',
    szLastName varchar(128) default '' comment '球员last name',
    szName varchar(1024) default '' comment '球员全名',
    szTeamName varchar(128) default '' comment '球队名',
    szPhotoUrl varchar(1024) default '' comment '球员照片URL',
    szPosition varchar(128) default '' comment '全员位置',
    szBirthDay varchar(128) default '' comment '球员生日',
    iWeight int unsigned not null default 0 comment '球员体重',
    iHeight int unsigned not null default 0 comment '球员身高',
    iShirtNum int unsigned not null default 0 comment '球衣号码',
    szCountry varchar(1024) default '' comment '球员国籍',
    iAge int unsigned not null default 0 comment '球员年龄',
    primary key (`iPlayerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='球员信息表';

create table IF NOT EXISTS tbTeamInfo(
    iTeamID int unsigned not null default 0 comment '球队ID',
    szTeamName varchar(128) default '' comment '球队名',
    primary key (`iTeamID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='球队信息表';
