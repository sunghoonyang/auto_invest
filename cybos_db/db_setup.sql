-- SET UP CYBOS DB
DROP DATABASE IF EXISTS cybos
;
CREATE DATABASE cybos
CHARACTER SET UTF8
COLLATE UTF8_GENERAL_CI
;

USE cybos
;

CREATE TABLESPACE `ts_cybos_1` ADD DATAFILE 'ts_cybos_1.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB
;

DROP TABLE IF EXISTS cybos.market_eye_today
;

CREATE TABLE cybos.market_eye_today (
    SEQ BIGINT AUTO_INCREMENT,
    `종목코드` varchar(64),
    `시간` SMALLINT,
    `대비부호` TINYINT,
    `전일대비` INT,
    `현재가` INT,
    `시가` INT,
    `고가` INT,
    `저가` INT,
    `매도호가` INT,
    `매수호가` INT,
    `거래량` INT,
    `거래대금` BIGINT,
    `장구분` INT,
    `총매도호가잔량` INT,
    `총매수호가잔량` INT,
    `최우선매도호가잔량` INT,
    `최우선매수호가잔량` INT,
    `종목명` NVARCHAR(128),
    `총상장주식수` BIGINT,
    `외국인보유비율` NUMERIC(23, 13),
    `전일거래량` INT,
    `전일종가` INT,
    `체결강도` NUMERIC(23, 10),
    `체결구분` TINYINT,
    `미결제약정` SMALLINT,
    `예상체결가` INT,
    `예상체결전일대비` INT,
    `예상체결대비부호` TINYINT,
    `예상체결수량` INT,
    `19일종가합` INT,
    `상한가` INT,
    `하한가` INT,
    `매매수량단위` SMALLINT,
    `시간외단일대비부호` TINYINT,
    `시간외단일전일대비` INT,
    `시간외단일현재가` INT,
    `시간외단일시가` INT,
    `시간외단일고가` INT,
    `시간외단일저가` INT,
    `시간외단일매도호가` INT,
    `시간외단일매수호가` INT,
    `시간외단일거래량` INT,
    `시간외단일거래대금` BIGINT,
    `시간외단일총매도호가잔량` INT,
    `시간외단일총매수호가잔량` INT,
    `시간외단일최우선매도호가잔량` INT,
    `시간외단일최우선매수호가잔량` INT,
    `시간외단일체결강도` INT,
    `시간외단일체결구분` INT,
    `시간외단일예상_실체결구분` INT,
    `시간외단일예상체결가` INT,
    `시간외단일예상체결전일대비` INT,
    `시간외단일예상체결대비부호` INT,
    `시간외단일예상체결수량` INT,
    `시간외단일SB구분여부` INT,
    `시간외단일기준가` INT,
    `시간외단일상한가` INT,
    `시간외단일하한가` INT,
    `외국계순매매` INT,
    `52주최고가` INT,
    `52주최저가` INT,
    `연중최고가` INT,
    `연중최저가` INT,
    `PER` NUMERIC(19, 10),
    `시간외매수잔량` INT,
    `시간외매도잔량` INT,
    `EPS` INT,
    `자본금` INT,
    `액면가` INT,
    `배당률` INT,
    `배당수익률` NUMERIC(23, 13),
    `부채비율` NUMERIC(23, 13),
    `유보율` NUMERIC(23, 9),
    `자기자본이익률` INT,
    `매출액증가율` NUMERIC(23, 13),
    `경상이익증가율` NUMERIC(23, 13),
    `순이익증가율` NUMERIC(23, 13),
    `투자심리` INT,
    `VR` INT,
    `5일회전률` NUMERIC(23, 13),
    `4일종가합` INT,
    `9일종가합` INT,
    `매출액` INT,
    `경상이익` BIGINT,
    `당기순이익` BIGINT,
    `BPS` INT,
    `영업이익증가율` NUMERIC(23, 13),
    `영업이익` BIGINT,
    `매출액영업이익률` NUMERIC(23, 13),
    `매출액경상이익률` NUMERIC(23, 13),
    `이자보상비율` NUMERIC(23, 16),
    `결산년월` VARCHAR(24),
    `분기BPS` INT,
    `분기매출액증가율` NUMERIC(23, 13),
    `분기영업이익증가율` NUMERIC(23, 13),
    `분기경상이익증가율` NUMERIC(23, 13),
    `분기순이익증가율` NUMERIC(23, 13),
    `분기매출액` INT,
    `분기영업이익` BIGINT,
    `분기경상이익` BIGINT,
    `분기당기순이익` BIGINT,
    `분기매출액영업이익률` NUMERIC(23, 13),
    `분기매출액경상이익률` NUMERIC(23, 13),
    `분기ROE` NUMERIC(23, 13),
    `분기이자보상비율` INT,
    `분기유보율` NUMERIC(23, 16),
    `분기부채비율` NUMERIC(23, 13),
    `최근분기년월` VARCHAR(24),
    `BASIS` INT,
    `현지날짜` BIGINT,
    `국가명` VARCHAR(64),
    `ELW_이론가` INT,
    `프로그램순매수` INT,
    `당일외국인순매수잠정구분` INT,
    `당일외국인순매수` INT,
    `당일기관순매수잠정구분` INT,
    `당일기관순매수` INT,
    `전일외국인순매수` INT,
    `전일기관순매수` INT,
    `SPS` BIGINT,
    `CFPS` BIGINT,
    `EBITDA` BIGINT,
    `신용잔고율` NUMERIC(23, 5),
    `공매도수량` BIGINT,
    `공매도일자` BIGINT,
    `ELW_E_기어링` BIGINT,
    `ELW_LP보유량` BIGINT,
    `ELW_LP보유율` INT,
    `ELW_Moneyness` INT,
    `ELW_Moneyness구분` INT,
    `ELW_감마` INT,
    `ELW_기어링` INT,
    `ELW_내재변동성` INT,
    `ELW_델타` INT,
    `ELW_발행수량` BIGINT,
    `ELW_베가` INT,
    `ELW_세타` INT,
    `ELW_손익분기율` INT,
    `ELW_역사적변동성` INT,
    `ELW_자본지지점` INT,
    `ELW_패리티` INT,
    `ELW_프리미엄` INT,
    `ELW_베리어` INT,
    QUERY_DT TIMESTAMP COMMENT '쿼리시간',
    LOAD_DT TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '적재시간',
    PRIMARY KEY (SEQ),
    UNIQUE KEY `stock_at_t` (`종목코드`, `현지날짜`, `시간`)
)
ENGINE = INNODB
;

DROP TABLE IF EXISTS cybos.market_eye_history
;

CREATE TABLE cybos.market_eye_history (
    SEQ BIGINT AUTO_INCREMENT,
    `종목코드` MEDIUMINT,
    `시간` SMALLINT,
    `대비부호` TINYINT,
    `전일대비` INT,
    `현재가` INT,
    `시가` INT,
    `고가` INT,
    `저가` INT,
    `매도호가` INT,
    `매수호가` INT,
    `거래량` INT,
    `거래대금` BIGINT,
    `장구분` INT,
    `총매도호가잔량` INT,
    `총매수호가잔량` INT,
    `최우선매도호가잔량` INT,
    `최우선매수호가잔량` INT,
    `종목명` NVARCHAR(128),
    `총상장주식수` BIGINT,
    `외국인보유비율` NUMERIC(23, 13),
    `전일거래량` INT,
    `전일종가` INT,
    `체결강도` NUMERIC(23, 10),
    `체결구분` TINYINT,
    `미결제약정` SMALLINT,
    `예상체결가` INT,
    `예상체결전일대비` INT,
    `예상체결대비부호` TINYINT,
    `예상체결수량` INT,
    `19일종가합` INT,
    `상한가` INT,
    `하한가` INT,
    `매매수량단위` SMALLINT,
    `시간외단일대비부호` TINYINT,
    `시간외단일전일대비` INT,
    `시간외단일현재가` INT,
    `시간외단일시가` INT,
    `시간외단일고가` INT,
    `시간외단일저가` INT,
    `시간외단일매도호가` INT,
    `시간외단일매수호가` INT,
    `시간외단일거래량` INT,
    `시간외단일거래대금` BIGINT,
    `시간외단일총매도호가잔량` INT,
    `시간외단일총매수호가잔량` INT,
    `시간외단일최우선매도호가잔량` INT,
    `시간외단일최우선매수호가잔량` INT,
    `시간외단일체결강도` INT,
    `시간외단일체결구분` INT,
    `시간외단일예상_실체결구분` INT,
    `시간외단일예상체결가` INT,
    `시간외단일예상체결전일대비` INT,
    `시간외단일예상체결대비부호` INT,
    `시간외단일예상체결수량` INT,
    `시간외단일SB구분여부` INT,
    `시간외단일기준가` INT,
    `시간외단일상한가` INT,
    `시간외단일하한가` INT,
    `외국계순매매` INT,
    `52주최고가` INT,
    `52주최저가` INT,
    `연중최고가` INT,
    `연중최저가` INT,
    `PER` NUMERIC(19, 10),
    `시간외매수잔량` INT,
    `시간외매도잔량` INT,
    `EPS` INT,
    `자본금` INT,
    `액면가` INT,
    `배당률` INT,
    `배당수익률` NUMERIC(23, 13),
    `부채비율` NUMERIC(23, 13),
    `유보율` NUMERIC(23, 9),
    `자기자본이익률` INT,
    `매출액증가율` NUMERIC(23, 13),
    `경상이익증가율` NUMERIC(23, 13),
    `순이익증가율` NUMERIC(23, 13),
    `투자심리` INT,
    `VR` INT,
    `5일회전률` NUMERIC(23, 13),
    `4일종가합` INT,
    `9일종가합` INT,
    `매출액` INT,
    `경상이익` BIGINT,
    `당기순이익` BIGINT,
    `BPS` INT,
    `영업이익증가율` NUMERIC(23, 13),
    `영업이익` BIGINT,
    `매출액영업이익률` NUMERIC(23, 13),
    `매출액경상이익률` NUMERIC(23, 13),
    `이자보상비율` NUMERIC(23, 16),
    `결산년월` VARCHAR(24),
    `분기BPS` INT,
    `분기매출액증가율` NUMERIC(23, 13),
    `분기영업이익증가율` NUMERIC(23, 13),
    `분기경상이익증가율` NUMERIC(23, 13),
    `분기순이익증가율` NUMERIC(23, 13),
    `분기매출액` INT,
    `분기영업이익` BIGINT,
    `분기경상이익` BIGINT,
    `분기당기순이익` BIGINT,
    `분기매출액영업이익률` NUMERIC(23, 13),
    `분기매출액경상이익률` NUMERIC(23, 13),
    `분기ROE` NUMERIC(23, 13),
    `분기이자보상비율` INT,
    `분기유보율` NUMERIC(23, 16),
    `분기부채비율` NUMERIC(23, 13),
    `최근분기년월` VARCHAR(24),
    `BASIS` INT,
    `현지날짜` BIGINT,
    `국가명` VARCHAR(64),
    `ELW_이론가` INT,
    `프로그램순매수` INT,
    `당일외국인순매수잠정구분` INT,
    `당일외국인순매수` INT,
    `당일기관순매수잠정구분` INT,
    `당일기관순매수` INT,
    `전일외국인순매수` INT,
    `전일기관순매수` INT,
    `SPS` BIGINT,
    `CFPS` BIGINT,
    `EBITDA` BIGINT,
    `신용잔고율` NUMERIC(23, 5),
    `공매도수량` BIGINT,
    `공매도일자` BIGINT,
    `ELW_E_기어링` BIGINT,
    `ELW_LP보유량` BIGINT,
    `ELW_LP보유율` INT,
    `ELW_Moneyness` INT,
    `ELW_Moneyness구분` INT,
    `ELW_감마` INT,
    `ELW_기어링` INT,
    `ELW_내재변동성` INT,
    `ELW_델타` INT,
    `ELW_발행수량` BIGINT,
    `ELW_베가` INT,
    `ELW_세타` INT,
    `ELW_손익분기율` INT,
    `ELW_역사적변동성` INT,
    `ELW_자본지지점` INT,
    `ELW_패리티` INT,
    `ELW_프리미엄` INT,
    `ELW_베리어` INT,
    `우선주_yn` CHAR(1),
    QUERY_DT TIMESTAMP COMMENT '쿼리시간',
    LOAD_DT TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '적재시간',
    PRIMARY KEY (SEQ),
    UNIQUE KEY `stock_at_t` (`종목코드`, `우선주_yn`, `현지날짜`, `시간`)
)
TABLESPACE ts_cybos_1 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
;

CREATE OR REPLACE VIEW cybos.vw_today_stock_info
AS
select
	l.stock_code
    , l.stock_name
    , l.volume
    , l.price
    , concat(l.latest_d, l.latest_t) as ts
    from (
	select
		h.`종목코드` as stock_code
		, h.`종목명` as stock_name
		, max(h.`현지날짜`) as latest_d
		, max(h.`시간`) as latest_t
		, h.`현재가` as price
		, h.`거래량` as volume
	from cybos.market_eye_today h
	group by 1, 2
    ) l
;
CREATE OR REPLACE VIEW cybos.vw_market_eye_latest
AS
SELECT
	*
FROM
	cybos.market_eye_history
WHERE
	`현지날짜` = (
	SELECT max(`현지날짜`)
	FROM cybos.market_eye_history
	)
ORDER BY `종목코드`, `현지날짜`, `시간` ASC
;

DROP TABLE IF EXISTS cybos.dim_krx_stock
;

CREATE TABLESPACE `ts_krx_1` ADD DATAFILE 'ts_krx_1.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB
;

CREATE TABLE cybos.dim_krx_stock (
	`종목코드` int,
    `종목명` varchar(128),
    `업종코드` mediumint,
    `업종` varchar(256),
	`주식시장타입` varchar(48),
    use_yn char(1) default 'N',
    PRIMARY KEY (`종목코드`),
    INDEX `indus_cd` (`업종코드`)
)
;

-- for data ingestion from api
CREATE TABLE cybos.`tbl_dailystock` (
  `item_cd` varchar(128) DEFAULT NULL,
  `day_Date` varchar(128) DEFAULT NULL,
  `day_Dungrak` varchar(128) DEFAULT NULL,
  `day_EndPrice` varchar(128) DEFAULT NULL,
  `day_High` varchar(128) DEFAULT NULL,
  `day_Low` varchar(128) DEFAULT NULL,
  `day_Start` varchar(128) DEFAULT NULL,
  `day_Volume` varchar(128) DEFAULT NULL,
  `day_getAmount` varchar(128) DEFAULT NULL,
  `day_getDebi` varchar(128) DEFAULT NULL,
  UNIQUE KEY `stock_at_t` (`item_cd`, `day_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

DROP TABLE IF EXISTS `cybos`.`tbl_timeconclude`
;
-- for data ingestion from api
CREATE TABLE `cybos`.`tbl_timeconclude` (
  `item_cd` varchar(255) DEFAULT NULL,
  `Debi` varchar(255) DEFAULT NULL,
  `Dungrak` varchar(255) DEFAULT NULL,
  `amount` varchar(255) DEFAULT NULL,
  `buyprice` varchar(255) DEFAULT NULL,
  `negoprice` varchar(255) DEFAULT NULL,
  `sellprice` varchar(255) DEFAULT NULL,
  `time` TIMESTAMP,
  UNIQUE KEY(`item_cd`, `time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE cybos.krx_dailystock_today (
    `item_cd` MEDIUMINT NOT NULL,
    `day_Date` TIMESTAMP NOT NULL,
    `day_Dungrak` SMALLINT,
    `day_EndPrice` numeric(11, 2),
    `day_High` numeric(11, 2),
    `day_Low` numeric(11, 2),
    `day_Start` numeric(11, 2),
    `day_Volume` numeric(11, 2),
    `day_getAmount`BIGINT,
    `day_getDebi` MEDIUMINT,
    PRIMARY KEY `stock_at_t` (`item_cd`, `day_date`)
)
;

CREATE TABLE cybos.krx_timeconclude_today (
    `item_cd` mediumint NOT NULL,
    `Debi` SMALLINT,
    `Dungrak` TINYINT,
    `amount` INT,
    `buyprice` decimal(11, 2),
    `negoprice` decimal(11, 2),
    `sellprice` decimal(11, 2),
    `time` TIMESTAMP,
    PRIMARY KEY(`item_cd`, `time`)
)
;

CREATE TABLE cybos.krx_dailystock_history (
    seq bigint auto_increment,
    `code` MEDIUMINT,
    `day_Date` TIMESTAMP,
    `day_Dungrak` SMALLINT,
    `day_EndPrice` numeric(11, 2),
    `day_High` numeric(11, 2),
    `day_Low` numeric(11, 2),
    `day_Start` numeric(11, 2),
    `day_Volume` numeric(11, 2),
    `day_getAmount`BIGINT,
    `day_getDebi` MEDIUMINT,
    PRIMARY KEY (seq),
    UNIQUE KEY `stock_at_t` (`code`, `day_date`)
)
TABLESPACE ts_krx_1 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8
;

CREATE TABLE cybos.krx_timeconclude_history (
    seq bigint auto_increment,
    `code` mediumint,
    `Debi` SMALLINT,
    `Dungrak` TINYINT,
    `amount` INT,
    `buyprice` decimal(11, 2),
    `negoprice` decimal(11, 2),
    `sellprice` decimal(11, 2),
    `time` TIMESTAMP,
    PRIMARY KEY(SEQ),
    UNIQUE KEY(`code`, `time`)
)
TABLESPACE ts_krx_1 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8
;