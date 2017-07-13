DELIMITER $$
DROP PROCEDURE IF EXISTS cybos.sp_market_eye_today_to_history$$
CREATE PROCEDURE cybos.sp_market_eye_today_to_history(IN p_today_date INT)
BEGIN
    DECLARE insert_rec INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
		BEGIN
			ROLLBACK;
		END;
	BEGIN
		INSERT INTO cybos.market_eye_history
			(`종목코드`, `시간`, `대비부호`, `전일대비`, `현재가`, `시가`, `고가`, `저가`, `매도호가`, `매수호가`, `거래량`, `거래대금`, `장구분`, `총매도호가잔량`, `총매수호가잔량`, `최우선매도호가잔량`, `최우선매수호가잔량`, `종목명`, `총상장주식수`, `외국인보유비율`, `전일거래량`, `전일종가`, `체결강도`, `체결구분`, `미결제약정`, `예상체결가`, `예상체결전일대비`, `예상체결대비부호`, `예상체결수량`, `19일종가합`, `상한가`, `하한가`, `매매수량단위`, `시간외단일대비부호`, `시간외단일전일대비`, `시간외단일현재가`, `시간외단일시가`, `시간외단일고가`, `시간외단일저가`, `시간외단일매도호가`, `시간외단일매수호가`, `시간외단일거래량`, `시간외단일거래대금`, `시간외단일총매도호가잔량`, `시간외단일총매수호가잔량`, `시간외단일최우선매도호가잔량`, `시간외단일최우선매수호가잔량`, `시간외단일체결강도`, `시간외단일체결구분`, `시간외단일예상_실체결구분`, `시간외단일예상체결가`, `시간외단일예상체결전일대비`, `시간외단일예상체결대비부호`, `시간외단일예상체결수량`, `시간외단일SB구분여부`, `시간외단일기준가`, `시간외단일상한가`, `시간외단일하한가`, `외국계순매매`, `52주최고가`, `52주최저가`, `연중최고가`, `연중최저가`, `PER`, `시간외매수잔량`, `시간외매도잔량`, `EPS`, `자본금`, `액면가`, `배당률`, `배당수익률`, `부채비율`, `유보율`, `자기자본이익률`, `매출액증가율`, `경상이익증가율`, `순이익증가율`, `투자심리`, `VR`, `5일회전률`, `4일종가합`, `9일종가합`, `매출액`, `경상이익`, `당기순이익`, `BPS`, `영업이익증가율`, `영업이익`, `매출액영업이익률`, `매출액경상이익률`, `이자보상비율`, `결산년월`, `분기BPS`, `분기매출액증가율`, `분기영업이익증가율`, `분기경상이익증가율`, `분기순이익증가율`, `분기매출액`, `분기영업이익`, `분기경상이익`, `분기당기순이익`, `분기매출액영업이익률`, `분기매출액경상이익률`, `분기ROE`, `분기이자보상비율`, `분기유보율`, `분기부채비율`, `최근분기년월`, `BASIS`, `현지날짜`, `국가명`, `ELW_이론가`, `프로그램순매수`, `당일외국인순매수잠정구분`, `당일외국인순매수`, `당일기관순매수잠정구분`, `당일기관순매수`, `전일외국인순매수`, `전일기관순매수`, `SPS`, `CFPS`, `EBITDA`, `신용잔고율`, `공매도수량`, `공매도일자`, `ELW_E_기어링`, `ELW_LP보유량`, `ELW_LP보유율`, `ELW_Moneyness`, `ELW_Moneyness구분`, `ELW_감마`, `ELW_기어링`, `ELW_내재변동성`, `ELW_델타`, `ELW_발행수량`, `ELW_베가`, `ELW_세타`, `ELW_손익분기율`, `ELW_역사적변동성`, `ELW_자본지지점`, `ELW_패리티`, `ELW_프리미엄`, `ELW_베리어`, `QUERY_DT`)
		SELECT
			`종목코드`, `시간`, `대비부호`, `전일대비`, `현재가`, `시가`, `고가`, `저가`, `매도호가`, `매수호가`, `거래량`, `거래대금`, `장구분`, `총매도호가잔량`, `총매수호가잔량`, `최우선매도호가잔량`, `최우선매수호가잔량`, `종목명`, `총상장주식수`, `외국인보유비율`, `전일거래량`, `전일종가`, `체결강도`, `체결구분`, `미결제약정`, `예상체결가`, `예상체결전일대비`, `예상체결대비부호`, `예상체결수량`, `19일종가합`, `상한가`, `하한가`, `매매수량단위`, `시간외단일대비부호`, `시간외단일전일대비`, `시간외단일현재가`, `시간외단일시가`, `시간외단일고가`, `시간외단일저가`, `시간외단일매도호가`, `시간외단일매수호가`, `시간외단일거래량`, `시간외단일거래대금`, `시간외단일총매도호가잔량`, `시간외단일총매수호가잔량`, `시간외단일최우선매도호가잔량`, `시간외단일최우선매수호가잔량`, `시간외단일체결강도`, `시간외단일체결구분`, `시간외단일예상_실체결구분`, `시간외단일예상체결가`, `시간외단일예상체결전일대비`, `시간외단일예상체결대비부호`, `시간외단일예상체결수량`, `시간외단일SB구분여부`, `시간외단일기준가`, `시간외단일상한가`, `시간외단일하한가`, `외국계순매매`, `52주최고가`, `52주최저가`, `연중최고가`, `연중최저가`, `PER`, `시간외매수잔량`, `시간외매도잔량`, `EPS`, `자본금`, `액면가`, `배당률`, `배당수익률`, `부채비율`, `유보율`, `자기자본이익률`, `매출액증가율`, `경상이익증가율`, `순이익증가율`, `투자심리`, `VR`, `5일회전률`, `4일종가합`, `9일종가합`, `매출액`, `경상이익`, `당기순이익`, `BPS`, `영업이익증가율`, `영업이익`, `매출액영업이익률`, `매출액경상이익률`, `이자보상비율`, `결산년월`, `분기BPS`, `분기매출액증가율`, `분기영업이익증가율`, `분기경상이익증가율`, `분기순이익증가율`, `분기매출액`, `분기영업이익`, `분기경상이익`, `분기당기순이익`, `분기매출액영업이익률`, `분기매출액경상이익률`, `분기ROE`, `분기이자보상비율`, `분기유보율`, `분기부채비율`, `최근분기년월`, `BASIS`, `현지날짜`, `국가명`, `ELW_이론가`, `프로그램순매수`, `당일외국인순매수잠정구분`, `당일외국인순매수`, `당일기관순매수잠정구분`, `당일기관순매수`, `전일외국인순매수`, `전일기관순매수`, `SPS`, `CFPS`, `EBITDA`, `신용잔고율`, `공매도수량`, `공매도일자`, `ELW_E_기어링`, `ELW_LP보유량`, `ELW_LP보유율`, `ELW_Moneyness`, `ELW_Moneyness구분`, `ELW_감마`, `ELW_기어링`, `ELW_내재변동성`, `ELW_델타`, `ELW_발행수량`, `ELW_베가`, `ELW_세타`, `ELW_손익분기율`, `ELW_역사적변동성`, `ELW_자본지지점`, `ELW_패리티`, `ELW_프리미엄`, `ELW_베리어`, `QUERY_DT`
			FROM cybos.market_eye_today
			WHERE `현지날짜` = p_today_date;
		SELECT @insert_rec := ROW_COUNT();
		DELETE FROM cybos.market_eye_today
			WHERE `현지날짜` = p_today_date;
		SELECT @insert_rec;
    END;
END;
$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS cybos.sp_krx_today_to_history$$
CREATE PROCEDURE cybos.sp_krx_today_to_history()
    BEGIN
        DECLARE dailystock_insert_rec dailystock INT;
        DECLARE timeconclude_insert_rec INT;
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
            END;
        BEGIN
        INSERT INTO cybos.krx_dailystock_history
            (`code`, `day_Date`, `day_Dungrak`, `day_EndPrice`, `day_High`, `day_Low`, `day_Start`, `day_Volume`, `day_getAmount`, `day_getDebi`)
        SELECT
            CAST(`tbl_dailystock`.`item_cd` AS UNSIGNED),
            STR_TO_DATE(`tbl_dailystock`.`day_Date`, '%d/%m/%y'),
            CAST(`day_EndPrice` AS DECIMAL(11, 2)),
            CAST(`day_High` AS DECIMAL(11, 2)),
            CAST(`day_Low` AS DECIMAL(11, 2)),
            CAST(`day_Start` AS DECIMAL(11, 2)),
            CAST(`day_Volume` AS DECIMAL(11, 2)),
            CAST(`tbl_dailystock` AS UNSIGNED),
            CAST(`day_getDebi` AS UNSIGNED)
        FROM `cybos`.`tbl_dailystock`
        GROUP BY 1, 2
        ;
        SELECT @dailystock_insert_rec := ROW_COUNT();
        INSERT INTO cybos.krx_timeconclude_history
            (`code`, `time`, Debi, Dungrak, amount, buyprice, negoprice, sellprice)
        SELECT
            CAST(CAST(`item_cd` AS DECIMAL(11, 0)) as UNSIGNED),
            timestamp(concat(curdate(), ' ', `time`)) ,
            CAST(CAST(`Debi` AS DECIMAL(11, 0)) as UNSIGNED),
            CAST(CAST(`Dungrak` AS DECIMAL(11, 0)) as UNSIGNED),
            CAST(CAST(`amount` AS DECIMAL(11, 0)) as UNSIGNED),
            CAST(`buyprice` AS DECIMAL(11, 2)),
            CAST(`negoprice` AS DECIMAL(11, 2)),
            CAST(`sellprice` AS DECIMAL(11, 2))
        FROM `cybos`.`tbl_timeconclude`
        GROUP BY 1, 2
        ;
        SELECT @timeconclude_insert_rec := ROW_COUNT();
        SELECT @timeconclude_insert_rec, @dailystock_insert_rec;
        END;
    END;
$$
DELIMITER ;